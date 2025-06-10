from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction, connection
from django.db.models import Count, Q
from datetime import timedelta
from scores.models import CachedAPIResponse, APICallLog, UserFavorite, UserSearchHistory
import logging
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Perform database maintenance tasks including optimization, cleanup, and integrity checks'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--optimize',
            action='store_true',
            help='Optimize database tables and indexes',
        )
        parser.add_argument(
            '--integrity-check',
            action='store_true',
            help='Perform database integrity checks',
        )
        parser.add_argument(
            '--cleanup-duplicates',
            action='store_true',
            help='Remove duplicate cache entries',
        )
        parser.add_argument(
            '--vacuum',
            action='store_true',
            help='Vacuum database to reclaim space (SQLite only)',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Display database statistics',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Starting database maintenance...')
        
        if options['stats']:
            self.display_database_stats()
        
        if options['integrity_check']:
            self.perform_integrity_check()
        
        if options['cleanup_duplicates']:
            self.cleanup_duplicate_cache_entries()
        
        if options['optimize']:
            self.optimize_database()
        
        if options['vacuum']:
            self.vacuum_database()
        
        self.stdout.write(
            self.style.SUCCESS('Database maintenance completed successfully')
        )
    
    def display_database_stats(self):
        """Display comprehensive database statistics"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('DATABASE STATISTICS')
        self.stdout.write('='*60)
        
        try:
            # Cache statistics
            total_cache = CachedAPIResponse.objects.count()
            expired_cache = CachedAPIResponse.objects.filter(
                expires_at__lte=timezone.now()
            ).count()
            active_cache = total_cache - expired_cache
            
            # API call statistics
            total_api_calls = APICallLog.objects.count()
            successful_calls = APICallLog.objects.filter(success=True).count()
            failed_calls = total_api_calls - successful_calls
            
            # User data statistics
            total_favorites = UserFavorite.objects.count()
            total_searches = UserSearchHistory.objects.count()
            
            # Cache hit rate calculation
            cache_entries_with_hits = CachedAPIResponse.objects.filter(
                hit_count__gt=0
            ).count()
            cache_hit_rate = (cache_entries_with_hits / total_cache * 100) if total_cache > 0 else 0
            
            # Display statistics
            self.stdout.write(f'Cache Entries:')
            self.stdout.write(f'  Total: {total_cache}')
            self.stdout.write(f'  Active: {active_cache}')
            self.stdout.write(f'  Expired: {expired_cache}')
            self.stdout.write(f'  Hit Rate: {cache_hit_rate:.2f}%')
            
            self.stdout.write(f'\nAPI Calls:')
            self.stdout.write(f'  Total: {total_api_calls}')
            self.stdout.write(f'  Successful: {successful_calls}')
            self.stdout.write(f'  Failed: {failed_calls}')
            
            if total_api_calls > 0:
                success_rate = (successful_calls / total_api_calls * 100)
                self.stdout.write(f'  Success Rate: {success_rate:.2f}%')
            
            self.stdout.write(f'\nUser Data:')
            self.stdout.write(f'  Favorites: {total_favorites}')
            self.stdout.write(f'  Search History: {total_searches}')
            
            # Top endpoints by cache usage
            top_endpoints = CachedAPIResponse.objects.values('endpoint').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
            
            if top_endpoints:
                self.stdout.write(f'\nTop Cached Endpoints:')
                for i, endpoint in enumerate(top_endpoints, 1):
                    self.stdout.write(f'  {i}. {endpoint["endpoint"]}: {endpoint["count"]} entries')
            
            self.stdout.write('='*60 + '\n')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error displaying database stats: {str(e)}')
            )
            logger.error(f'Database stats error: {str(e)}', exc_info=True)
    
    def perform_integrity_check(self):
        """Perform database integrity checks"""
        self.stdout.write('Performing database integrity checks...')
        
        issues_found = 0
        
        try:
            # Check for cache entries with invalid JSON
            self.stdout.write('Checking cache entries for invalid JSON...')
            invalid_json_count = 0
            
            for cache_entry in CachedAPIResponse.objects.all():
                try:
                    if cache_entry.response_data:
                        json.dumps(cache_entry.response_data)
                    if cache_entry.parameters:
                        json.dumps(cache_entry.parameters)
                except (TypeError, ValueError) as e:
                    invalid_json_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Invalid JSON in cache entry {cache_entry.id}: {str(e)}'
                        )
                    )
            
            if invalid_json_count > 0:
                issues_found += invalid_json_count
                self.stdout.write(
                    self.style.WARNING(f'Found {invalid_json_count} cache entries with invalid JSON')
                )
            else:
                self.stdout.write(self.style.SUCCESS('All cache entries have valid JSON'))
            
            # Check for orphaned cache entries (expired for too long)
            self.stdout.write('Checking for orphaned cache entries...')
            one_month_ago = timezone.now() - timedelta(days=30)
            orphaned_cache = CachedAPIResponse.objects.filter(
                expires_at__lte=one_month_ago
            ).count()
            
            if orphaned_cache > 0:
                issues_found += orphaned_cache
                self.stdout.write(
                    self.style.WARNING(f'Found {orphaned_cache} orphaned cache entries (expired >30 days)')
                )
            else:
                self.stdout.write(self.style.SUCCESS('No orphaned cache entries found'))
            
            # Check for duplicate cache keys
            self.stdout.write('Checking for duplicate cache keys...')
            duplicate_keys = CachedAPIResponse.objects.values('cache_key').annotate(
                count=Count('id')
            ).filter(count__gt=1)
            
            if duplicate_keys.exists():
                issues_found += duplicate_keys.count()
                self.stdout.write(
                    self.style.WARNING(f'Found {duplicate_keys.count()} duplicate cache keys')
                )
                for dup in duplicate_keys[:5]:  # Show first 5
                    self.stdout.write(f'  Duplicate key: {dup["cache_key"]} ({dup["count"]} entries)')
            else:
                self.stdout.write(self.style.SUCCESS('No duplicate cache keys found'))
            
            # Summary
            if issues_found == 0:
                self.stdout.write(
                    self.style.SUCCESS('Database integrity check completed - no issues found')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Database integrity check completed - {issues_found} issues found')
                )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during integrity check: {str(e)}')
            )
            logger.error(f'Integrity check error: {str(e)}', exc_info=True)
    
    def cleanup_duplicate_cache_entries(self):
        """Remove duplicate cache entries, keeping the most recent"""
        self.stdout.write('Cleaning up duplicate cache entries...')
        
        try:
            with transaction.atomic():
                # Find duplicate cache keys
                duplicate_keys = CachedAPIResponse.objects.values('cache_key').annotate(
                    count=Count('id')
                ).filter(count__gt=1)
                
                if not duplicate_keys.exists():
                    self.stdout.write('No duplicate cache entries found')
                    return
                
                removed_count = 0
                
                for dup_key in duplicate_keys:
                    cache_key = dup_key['cache_key']
                    
                    # Get all entries with this cache key, ordered by creation date (newest first)
                    entries = CachedAPIResponse.objects.filter(
                        cache_key=cache_key
                    ).order_by('-created_at')
                    
                    # Keep the first (newest) entry, delete the rest
                    entries_to_delete = entries[1:]
                    
                    for entry in entries_to_delete:
                        entry.delete()
                        removed_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'Removed {removed_count} duplicate cache entries')
                )
                logger.info(f'Cleaned up {removed_count} duplicate cache entries')
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error cleaning up duplicates: {str(e)}')
            )
            logger.error(f'Duplicate cleanup error: {str(e)}', exc_info=True)
    
    def optimize_database(self):
        """Optimize database performance"""
        self.stdout.write('Optimizing database...')
        
        try:
            with connection.cursor() as cursor:
                # For SQLite, analyze tables to update statistics
                if 'sqlite' in connection.vendor:
                    cursor.execute('ANALYZE')
                    self.stdout.write('Updated SQLite table statistics')
                
                # For PostgreSQL, analyze tables
                elif 'postgresql' in connection.vendor:
                    cursor.execute('ANALYZE')
                    self.stdout.write('Updated PostgreSQL table statistics')
                
                # For MySQL, optimize tables
                elif 'mysql' in connection.vendor:
                    tables = [
                        'scores_cachedapiresponse',
                        'scores_apicalllog',
                        'scores_userfavorite',
                        'scores_usersearchhistory'
                    ]
                    for table in tables:
                        try:
                            cursor.execute(f'OPTIMIZE TABLE {table}')
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(f'Could not optimize table {table}: {str(e)}')
                            )
                    self.stdout.write('Optimized MySQL tables')
            
            self.stdout.write(self.style.SUCCESS('Database optimization completed'))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error optimizing database: {str(e)}')
            )
            logger.error(f'Database optimization error: {str(e)}', exc_info=True)
    
    def vacuum_database(self):
        """Vacuum database to reclaim space (SQLite only)"""
        self.stdout.write('Vacuuming database...')
        
        try:
            if 'sqlite' in connection.vendor:
                with connection.cursor() as cursor:
                    cursor.execute('VACUUM')
                self.stdout.write(self.style.SUCCESS('Database vacuum completed'))
            else:
                self.stdout.write(
                    self.style.WARNING('Vacuum operation is only supported for SQLite databases')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error vacuuming database: {str(e)}')
            )
            logger.error(f'Database vacuum error: {str(e)}', exc_info=True)