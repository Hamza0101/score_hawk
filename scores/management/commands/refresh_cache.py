from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from datetime import timedelta
from scores.models import CachedAPIResponse, APICallLog
from scores.api_manager import CricketAPIManager
import logging
import json

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
            expired_entries = CachedAPIResponse.objects.all().select_related()
            self.stdout.write(f'Force refreshing {expired_entries.count()} cache entries')
        else:
            expired_entries = CachedAPIResponse.objects.filter(
                expires_at__lte=timezone.now()
            ).select_related()
            self.stdout.write(f'Found {expired_entries.count()} expired cache entries')
        
        if not expired_entries.exists():
            self.stdout.write(self.style.SUCCESS('No cache entries to refresh'))
            self.cleanup_expired_cache()
            return
        
        api_manager = CricketAPIManager()
        refreshed_count = 0
        failed_count = 0
        
        # Process entries in batches to avoid memory issues
        batch_size = 10
        total_entries = expired_entries.count()
        
        for i in range(0, total_entries, batch_size):
            batch = expired_entries[i:i + batch_size]
            
            for entry in batch:
                try:
                    with transaction.atomic():
                        self.stdout.write(f'Refreshing: {entry.endpoint} (Cache Key: {entry.cache_key})')
                        
                        # Validate and parse parameters
                        params = self._validate_parameters(entry.parameters)
                        
                        # Make fresh API request
                        fresh_data = api_manager.make_request(
                            entry.endpoint, 
                            params=params, 
                            cache_enabled=True
                        )
                        
                        if fresh_data:
                            # Verify data integrity
                            if self._validate_response_data(fresh_data):
                                refreshed_count += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f'✓ Refreshed: {entry.endpoint}')
                                )
                                
                                # Log successful refresh
                                self._log_refresh_success(entry, fresh_data)
                            else:
                                failed_count += 1
                                self.stdout.write(
                                    self.style.WARNING(f'⚠ Invalid data received for: {entry.endpoint}')
                                )
                                self._log_refresh_failure(entry, 'Invalid response data')
                        else:
                            failed_count += 1
                            self.stdout.write(
                                self.style.ERROR(f'✗ Failed to refresh: {entry.endpoint}')
                            )
                            self._log_refresh_failure(entry, 'No data received from API')
                            
                except Exception as e:
                    failed_count += 1
                    error_msg = str(e)
                    self.stdout.write(
                        self.style.ERROR(f'✗ Error refreshing {entry.endpoint}: {error_msg}')
                    )
                    self._log_refresh_failure(entry, error_msg)
                    logger.error(f'Cache refresh error for {entry.endpoint}: {error_msg}', exc_info=True)
        
        # Cleanup old expired entries
        self.cleanup_expired_cache()
        
        # Generate summary report
        self._generate_refresh_report(refreshed_count, failed_count, total_entries)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Cache refresh completed: {refreshed_count} refreshed, {failed_count} failed'
            )
        )
    
    def cleanup_expired_cache(self):
        """Remove expired cache entries from database with proper transaction handling"""
        try:
            with transaction.atomic():
                # Count expired entries
                expired_count = CachedAPIResponse.objects.filter(
                    expires_at__lte=timezone.now()
                ).count()
                
                if expired_count > 0:
                    # Delete expired entries in batches to avoid memory issues
                    batch_size = 100
                    deleted_total = 0
                    
                    while True:
                        expired_ids = list(
                            CachedAPIResponse.objects.filter(
                                expires_at__lte=timezone.now()
                            ).values_list('id', flat=True)[:batch_size]
                        )
                        
                        if not expired_ids:
                            break
                            
                        deleted_count = CachedAPIResponse.objects.filter(
                            id__in=expired_ids
                        ).delete()[0]
                        
                        deleted_total += deleted_count
                        
                        if deleted_count < batch_size:
                            break
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Cleaned up {deleted_total} expired cache entries')
                    )
                    logger.info(f'Cleaned up {deleted_total} expired cache entries')
                else:
                    self.stdout.write('No expired cache entries to clean up')
                
                # Cleanup very old entries (older than 2 weeks) with better query
                two_weeks_ago = timezone.now() - timedelta(weeks=2)
                old_entries = CachedAPIResponse.objects.filter(
                    Q(created_at__lte=two_weeks_ago) | Q(last_refreshed__lte=two_weeks_ago)
                )
                old_count = old_entries.count()
                
                if old_count > 0:
                    # Delete old entries in batches
                    deleted_old_total = 0
                    
                    while True:
                        old_ids = list(
                            CachedAPIResponse.objects.filter(
                                Q(created_at__lte=two_weeks_ago) | Q(last_refreshed__lte=two_weeks_ago)
                            ).values_list('id', flat=True)[:batch_size]
                        )
                        
                        if not old_ids:
                            break
                            
                        deleted_count = CachedAPIResponse.objects.filter(
                            id__in=old_ids
                        ).delete()[0]
                        
                        deleted_old_total += deleted_count
                        
                        if deleted_count < batch_size:
                            break
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Cleaned up {deleted_old_total} old cache entries (>2 weeks)')
                    )
                    logger.info(f'Cleaned up {deleted_old_total} old cache entries')
                
                # Cleanup orphaned API call logs (older than 1 month)
                one_month_ago = timezone.now() - timedelta(days=30)
                old_logs_count = APICallLog.objects.filter(
                    timestamp__lte=one_month_ago
                ).count()
                
                if old_logs_count > 0:
                    APICallLog.objects.filter(
                        timestamp__lte=one_month_ago
                    ).delete()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Cleaned up {old_logs_count} old API call logs (>1 month)')
                    )
                    logger.info(f'Cleaned up {old_logs_count} old API call logs')
                    
        except Exception as e:
            error_msg = f'Error during cache cleanup: {str(e)}'
            self.stdout.write(self.style.ERROR(error_msg))
            logger.error(error_msg, exc_info=True)
            raise
    
    def _validate_parameters(self, parameters):
        """Validate and sanitize parameters from cached entry"""
        if not parameters:
            return None
            
        if isinstance(parameters, str):
            try:
                return json.loads(parameters)
            except json.JSONDecodeError:
                logger.warning(f'Invalid JSON in parameters: {parameters}')
                return None
        
        if isinstance(parameters, dict):
            return parameters
            
        logger.warning(f'Unexpected parameter type: {type(parameters)}')
        return None
    
    def _validate_response_data(self, data):
        """Validate response data integrity"""
        if not data:
            return False
            
        # Basic validation - ensure it's a valid data structure
        if not isinstance(data, (dict, list)):
            return False
            
        # Check for common error indicators
        if isinstance(data, dict):
            error_indicators = ['error', 'Error', 'ERROR', 'message']
            for indicator in error_indicators:
                if indicator in data and 'error' in str(data[indicator]).lower():
                    return False
                    
        return True
    
    def _log_refresh_success(self, entry, data):
        """Log successful cache refresh"""
        try:
            data_size = len(json.dumps(data)) if data else 0
            logger.info(
                f'Successfully refreshed cache for {entry.endpoint} '
                f'(Key: {entry.cache_key}, Data size: {data_size} bytes)'
            )
        except Exception as e:
            logger.warning(f'Error logging refresh success: {e}')
    
    def _log_refresh_failure(self, entry, error_message):
        """Log failed cache refresh"""
        try:
            logger.error(
                f'Failed to refresh cache for {entry.endpoint} '
                f'(Key: {entry.cache_key}): {error_message}'
            )
        except Exception as e:
            logger.warning(f'Error logging refresh failure: {e}')
    
    def _generate_refresh_report(self, refreshed_count, failed_count, total_entries):
        """Generate and log detailed refresh report"""
        try:
            success_rate = (refreshed_count / total_entries * 100) if total_entries > 0 else 0
            
            report = {
                'timestamp': timezone.now().isoformat(),
                'total_entries': total_entries,
                'refreshed_count': refreshed_count,
                'failed_count': failed_count,
                'success_rate': round(success_rate, 2)
            }
            
            logger.info(f'Cache refresh report: {json.dumps(report, indent=2)}')
            
            # Display summary
            self.stdout.write('\n' + '='*50)
            self.stdout.write('CACHE REFRESH SUMMARY')
            self.stdout.write('='*50)
            self.stdout.write(f'Total entries processed: {total_entries}')
            self.stdout.write(f'Successfully refreshed: {refreshed_count}')
            self.stdout.write(f'Failed to refresh: {failed_count}')
            self.stdout.write(f'Success rate: {success_rate:.2f}%')
            self.stdout.write('='*50 + '\n')
            
        except Exception as e:
            logger.warning(f'Error generating refresh report: {e}')