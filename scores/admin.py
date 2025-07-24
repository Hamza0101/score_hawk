from django.contrib import admin
from .models import APICallLog, CachedAPIResponse, UserFavorite, UserSearchHistory

@admin.register(APICallLog)
class APICallLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'endpoint', 'success', 'response_time', 'status_code']
    list_filter = ['success', 'timestamp', 'endpoint']
    search_fields = ['user__email', 'endpoint', 'error_message']
    readonly_fields = ['timestamp', 'request_hash', 'response_time']
    ordering = ['-timestamp']

@admin.register(CachedAPIResponse)
class CachedAPIResponseAdmin(admin.ModelAdmin):
    list_display = ['cache_key', 'endpoint', 'created_at', 'expires_at', 'hit_count', 'is_expired']
    list_filter = ['endpoint', 'created_at', 'expires_at']
    search_fields = ['cache_key', 'endpoint']
    readonly_fields = ['created_at', 'hit_count']
    ordering = ['-created_at']
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_type', 'favorite_id', 'name', 'created_at']
    list_filter = ['favorite_type', 'created_at']
    search_fields = ['user__email', 'name', 'favorite_id']
    ordering = ['-created_at']

@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_term', 'search_type', 'results_count', 'timestamp']
    list_filter = ['search_type', 'timestamp']
    search_fields = ['user__email', 'search_term']
    ordering = ['-timestamp']
