import requests
import hashlib
import json
import time
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from .models import APICallLog, CachedAPIResponse
import logging

logger = logging.getLogger(__name__)

class CricketAPIManager:
    """Enhanced API manager with database logging and caching"""
    
    BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
    HEADERS = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    
    # Cache durations for different endpoints (in minutes)
    # Extended caching to minimize API calls - cache for 30 days
    CACHE_DURATIONS = {
        'news': 43200,        # 30 days (43200 minutes)
        'rankings': 43200,    # 30 days
        'matches': 43200,     # 30 days
        'player_stats': 43200, # 30 days
        'team_stats': 43200,  # 30 days
        'search': 43200,      # 30 days
        'detail': 43200,      # 30 days
        'stats': 43200,       # 30 days
        'default': 43200,     # 30 days for any other endpoint
    }
    
    def __init__(self, user=None, ip_address=None):
        self.user = user
        self.ip_address = ip_address
    
    def _generate_cache_key(self, endpoint, params=None):
        """Generate a unique cache key for the request"""
        params_str = json.dumps(params or {}, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f"api_cache_{endpoint.replace('/', '_')}_{params_hash}"
    
    def _get_cache_duration(self, endpoint):
        """Get cache duration based on endpoint type"""
        for key, duration in self.CACHE_DURATIONS.items():
            if key in endpoint:
                return duration
        return self.CACHE_DURATIONS['default']  # Default 1 week
    
    def _log_api_call(self, endpoint, method='GET', params=None, 
                     response_status=None, response_time=None, 
                     success=False, error_message=''):
        """Log API call to database"""
        try:
            APICallLog.objects.create(
                endpoint=endpoint,
                method=method,
                parameters=params or {},
                response_status=response_status,
                response_time=response_time,
                user=self.user,
                ip_address=self.ip_address,
                success=success,
                error_message=error_message
            )
        except Exception as e:
            logger.error(f"Failed to log API call: {e}")
    
    def _get_cached_response(self, cache_key):
        """Get cached response from database"""
        try:
            cached = CachedAPIResponse.objects.get(cache_key=cache_key)
            
            # Check if cache is still valid (within 30 days)
            if cached.expires_at > timezone.now():
                cached.hit_count += 1
                cached.last_refreshed = timezone.now()
                cached.save(update_fields=['hit_count', 'last_refreshed'])
                logger.info(f"Cache hit for {cache_key} - expires at {cached.expires_at}, hit count: {cached.hit_count}")
                return cached.response_data
            else:
                # Cache expired, but keep old data and refresh in background
                logger.info(f"Cache expired for {cache_key} - last updated {cached.created_at}, returning cached data")
                # Return cached data even if expired to avoid API calls
                cached.hit_count += 1
                cached.save(update_fields=['hit_count'])
                return cached.response_data
                
        except CachedAPIResponse.DoesNotExist:
            return None
    
    def _cache_response(self, cache_key, endpoint, params, data, duration_minutes):
        """Cache response in database"""
        try:
            params_hash = hashlib.md5(
                json.dumps(params or {}, sort_keys=True).encode()
            ).hexdigest()
            
            expires_at = timezone.now() + timedelta(minutes=duration_minutes)
            
            CachedAPIResponse.objects.update_or_create(
                cache_key=cache_key,
                defaults={
                    'endpoint': endpoint,
                    'parameters': params or {},  # Store actual parameters for refresh
                    'parameters_hash': params_hash,
                    'response_data': data,
                    'expires_at': expires_at,
                    'hit_count': 0
                }
            )
        except Exception as e:
            logger.error(f"Failed to cache response: {e}")
    
    def _get_empty_response_structure(self, endpoint):
        """Return appropriate empty structure based on endpoint type"""
        if 'news' in endpoint:
            return {'storyList': []}
        elif 'rankings' in endpoint or 'stats' in endpoint:
            return {'rank': []}
        elif 'matches' in endpoint:
            return {'typeMatches': []}
        elif 'player' in endpoint:
            return {'player': []}
        elif 'search' in endpoint:
            return {'player': []}
        else:
            return {}
    
    def make_request(self, endpoint, params=None, cache_enabled=True, force_cache=False):
        """Make API request with aggressive caching to minimize external calls"""
        full_url = f"{self.BASE_URL}{endpoint}"
        cache_key = self._generate_cache_key(endpoint, params)
        
        # Always try to get cached response first
        if cache_enabled:
            cached_data = self._get_cached_response(cache_key)
            if cached_data:
                logger.info(f"Cache hit for {endpoint} - using cached data")
                return cached_data
        
        # If force_cache is True, avoid making API calls and return empty data
        if force_cache:
            logger.info(f"Force cache enabled - avoiding API call for {endpoint}")
            # Return empty but valid structure to prevent errors
            return self._get_empty_response_structure(endpoint)
        
        # Make actual API request only if force_cache is False
        start_time = time.time()
        try:
            response = requests.get(full_url, headers=self.HEADERS, params=params)
            response_time = time.time() - start_time
            
            response.raise_for_status()
            data = response.json()
            
            # Log successful API call
            self._log_api_call(
                endpoint=endpoint,
                params=params,
                response_status=response.status_code,
                response_time=response_time,
                success=True
            )
            
            # Cache the response
            if cache_enabled:
                duration = self._get_cache_duration(endpoint)
                self._cache_response(cache_key, endpoint, params, data, duration)
            
            return data
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            error_message = str(e)
            
            # Log failed API call
            self._log_api_call(
                endpoint=endpoint,
                params=params,
                response_status=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                response_time=response_time,
                success=False,
                error_message=error_message
            )
            
            logger.error(f"API request failed for {endpoint}: {error_message}")
            # Return cached data even if API fails
            cached_data = self._get_cached_response(cache_key)
            if cached_data:
                logger.info(f"API failed, returning cached data for {endpoint}")
                return cached_data
            return self._get_empty_response_structure(endpoint)
        
        except Exception as e:
            response_time = time.time() - start_time
            error_message = str(e)
            
            self._log_api_call(
                endpoint=endpoint,
                params=params,
                response_time=response_time,
                success=False,
                error_message=error_message
            )
            
            logger.error(f"Unexpected error for {endpoint}: {error_message}")
            # Return cached data even if unexpected error
            cached_data = self._get_cached_response(cache_key)
            if cached_data:
                logger.info(f"Unexpected error, returning cached data for {endpoint}")
                return cached_data
            return self._get_empty_response_structure(endpoint)

# Convenience functions using the API manager with caching
def get_cricket_news(user=None, ip_address=None, force_cache=False):
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/news/v1/index', force_cache=force_cache)
    if data:
        return [item for item in data.get('storyList', []) if 'story' in item]
    return []

def get_news_detail(news_id, user=None, ip_address=None, force_cache=False):
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    return api_manager.make_request(f'/news/v1/detail/{news_id}', force_cache=force_cache)

def get_rankings(format_type='test', user=None, ip_address=None, force_cache=False):
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/rankings/teams', {'formatType': format_type}, force_cache=force_cache)
    if data:
        return [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
    return []