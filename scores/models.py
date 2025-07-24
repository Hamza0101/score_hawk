from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import json

User = get_user_model()

class APICallLog(models.Model):
    """Log all API calls for monitoring and analytics"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    endpoint = models.CharField(max_length=255)
    request_params = models.TextField(blank=True)
    request_hash = models.CharField(max_length=64, db_index=True)  # For quick cache lookups
    response_time = models.FloatField(help_text="Response time in seconds")
    status_code = models.IntegerField()
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['endpoint', '-timestamp']),
            models.Index(fields=['success', '-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.endpoint} - {self.timestamp}"

class CachedAPIResponse(models.Model):
    """Cache API responses to minimize external API calls"""
    cache_key = models.CharField(max_length=255, unique=True, db_index=True)
    endpoint = models.CharField(max_length=255, db_index=True)
    request_params_hash = models.CharField(max_length=64)
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)
    hit_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint', 'expires_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def increment_hit_count(self):
        self.hit_count += 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['hit_count', 'last_accessed'])
    
    def __str__(self):
        return f"{self.endpoint} - {self.cache_key[:20]}..."

class UserFavorite(models.Model):
    """Store user favorites for teams, players, matches, etc."""
    FAVORITE_TYPES = [
        ('team', 'Team'),
        ('player', 'Player'),
        ('match', 'Match'),
        ('venue', 'Venue'),
        ('series', 'Series'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    favorite_type = models.CharField(max_length=20, choices=FAVORITE_TYPES)
    favorite_id = models.CharField(max_length=100)  # External ID from cricket API
    name = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional info
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'favorite_type', 'favorite_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'favorite_type']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.favorite_type})"

class UserSearchHistory(models.Model):
    """Track user search history for better recommendations"""
    SEARCH_TYPES = [
        ('players', 'Players'),
        ('teams', 'Teams'),
        ('matches', 'Matches'),
        ('news', 'News'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    search_term = models.CharField(max_length=255)
    search_type = models.CharField(max_length=20, choices=SEARCH_TYPES, default='general')
    results_count = models.PositiveIntegerField(default=0)
    clicked_result = models.CharField(max_length=255, blank=True)  # Track what user clicked
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'search_type', '-timestamp']),
            models.Index(fields=['search_term', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} searched '{self.search_term}'"

class ChatMessage(models.Model):
    """Store chat messages between users and the AI chatbot"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    message = models.TextField()
    is_user = models.BooleanField(default=True)  # True for user messages, False for bot responses
    context_data = models.JSONField(default=dict, blank=True)  # Store context like current page, match ID, etc.
    response_time = models.FloatField(null=True, blank=True)  # Time taken to generate response
    tokens_used = models.IntegerField(null=True, blank=True)  # OpenAI tokens used
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['session_key', '-timestamp']),
            models.Index(fields=['is_user', '-timestamp']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else f"Anonymous:{self.session_key[:8]}"
        msg_type = "User" if self.is_user else "Bot"
        return f"{user_str} - {msg_type}: {self.message[:50]}..."

class ChatSession(models.Model):
    """Track chat sessions for analytics and context"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    message_count = models.PositiveIntegerField(default=0)
    total_tokens_used = models.PositiveIntegerField(default=0)
    context_page = models.CharField(max_length=100, blank=True)  # Page where chat started
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['session_key', '-started_at']),
            models.Index(fields=['is_active', '-last_activity']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else f"Anonymous:{self.session_key[:8]}"
        return f"Chat Session: {user_str} - {self.started_at}"
    
    def increment_message_count(self, tokens_used=0):
        self.message_count += 1
        self.total_tokens_used += tokens_used
        self.last_activity = timezone.now()
        self.save(update_fields=['message_count', 'total_tokens_used', 'last_activity'])
    
    def end_session(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

class UserPreference(models.Model):
    """Store user preferences for personalized experience"""
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    NOTIFICATION_CHOICES = [
        ('all', 'All Notifications'),
        ('favorites', 'Favorites Only'),
        ('important', 'Important Only'),
        ('none', 'No Notifications'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    favorite_teams = models.JSONField(default=list, blank=True)  # List of team IDs
    favorite_players = models.JSONField(default=list, blank=True)  # List of player IDs
    notification_settings = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES, default='all')
    live_score_refresh_interval = models.PositiveIntegerField(default=30)  # seconds
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} preferences"

class MatchAlert(models.Model):
    """User alerts for specific matches or events"""
    ALERT_TYPES = [
        ('match_start', 'Match Start'),
        ('innings_break', 'Innings Break'),
        ('wicket', 'Wicket'),
        ('boundary', 'Boundary (4/6)'),
        ('milestone', 'Milestone (50/100)'),
        ('match_end', 'Match End'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_alerts')
    match_id = models.CharField(max_length=100)
    match_name = models.CharField(max_length=255)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    is_active = models.BooleanField(default=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'match_id', 'alert_type']
        indexes = [
            models.Index(fields=['match_id', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.match_name} - {self.get_alert_type_display()}"
    
    def trigger_alert(self):
        self.triggered_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['triggered_at', 'is_active'])

class NewsBookmark(models.Model):
    """User bookmarked news articles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_news')
    news_id = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    thumbnail = models.URLField(blank=True)
    bookmarked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'news_id']
        ordering = ['-bookmarked_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked: {self.title[:50]}"