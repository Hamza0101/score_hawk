from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class APICallLog(models.Model):
    """Track all API calls for monitoring and caching"""
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10, default='GET')
    parameters = models.JSONField(default=dict, blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)  # in seconds
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['endpoint', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.endpoint} - {self.timestamp}"

class CachedAPIResponse(models.Model):
    """Cache API responses to reduce external API calls"""
    cache_key = models.CharField(max_length=255, unique=True)
    endpoint = models.CharField(max_length=255)
    parameters = models.JSONField(default=dict, blank=True)  # Store actual parameters
    parameters_hash = models.CharField(max_length=64)  # MD5 hash of parameters
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    hit_count = models.PositiveIntegerField(default=0)
    last_refreshed = models.DateTimeField(auto_now=True)  # Track when data was last updated
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cache_key']),
            models.Index(fields=['endpoint', 'expires_at']),
        ]
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"{self.endpoint} - {self.cache_key}"

class UserFavorite(models.Model):
    """Store user's favorite teams, players, etc."""
    FAVORITE_TYPES = [
        ('team', 'Team'),
        ('player', 'Player'),
        ('match', 'Match'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_type = models.CharField(max_length=10, choices=FAVORITE_TYPES)
    favorite_id = models.CharField(max_length=100)  # External API ID
    favorite_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'favorite_type', 'favorite_id']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.favorite_name}"

class UserSearchHistory(models.Model):
    """Track user search history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    search_type = models.CharField(max_length=50)  # 'player', 'team', 'news', etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    results_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.search_query}"
