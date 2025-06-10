from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from scores.models import CachedAPIResponse
from scores.api_manager import CricketAPIManager
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Refresh expired cache data and clean up old entries'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force-refresh',
            action='store_true',
            help='Force refresh all cached data regardless of expiration',
        )
        parser.add_argument(
            '--cleanup-only',
            action='store_true',
            help='Only cleanup expired entries without refreshing',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Starting cache refresh process...')
        
        if options['cleanup_only']:
            self.cleanup_expired_cache()
            return
        
        # Get expired or force refresh all cache entries
        if options['force_refresh']:
            expired_entries = CachedAPIResponse.objects.all()
            self.stdout.write(f'Force refreshing {expired_entries.count()} cache entries')
        else:
            expired_entries = CachedAPIResponse.objects.filter(
                expires_at__lte=timezone.now()
            )
            self.stdout.write(f'Found {expired_entries.count()} expired cache entries')
        
        api_manager = CricketAPIManager()
        refreshed_count = 0
        failed_count = 0
        
        for entry in expired_entries:
            try:
                self.stdout.write(f'Refreshing: {entry.endpoint}')
                
                # Parse parameters from the cached entry
                params = None
                if hasattr(entry, 'parameters') and entry.parameters:
                    params = entry.parameters
                
                # Make fresh API request
                fresh_data = api_manager.make_request(
                    entry.endpoint, 
                    params=params, 
                    cache_enabled=True
                )
                
                if fresh_data:
                    refreshed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Refreshed: {entry.endpoint}')
                    )
                else:
                    failed_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to refresh: {entry.endpoint}')
                    )
                    
            except Exception as e:
                failed_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Error refreshing {entry.endpoint}: {str(e)}')
                )
        
        # Cleanup old expired entries
        self.cleanup_expired_cache()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Cache refresh completed: {refreshed_count} refreshed, {failed_count} failed'
            )
        )
    
    def cleanup_expired_cache(self):
        """Remove expired cache entries from database"""
        expired_count = CachedAPIResponse.objects.filter(
            expires_at__lte=timezone.now()
        ).count()
        
        if expired_count > 0:
            CachedAPIResponse.objects.filter(
                expires_at__lte=timezone.now()
            ).delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Cleaned up {expired_count} expired cache entries')
            )
        else:
            self.stdout.write('No expired cache entries to clean up')
        
        # Also cleanup very old entries (older than 2 weeks)
        two_weeks_ago = timezone.now() - timedelta(weeks=2)
        old_count = CachedAPIResponse.objects.filter(
            created_at__lte=two_weeks_ago
        ).count()
        
        if old_count > 0:
            CachedAPIResponse.objects.filter(
                created_at__lte=two_weeks_ago
            ).delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Cleaned up {old_count} old cache entries (>2 weeks)')
            )