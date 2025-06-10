from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.management import call_command
from django.db.models import Sum, Count, Q, Avg
from django.db import models
from .cricbuzz_api import (get_cricket_news, get_news_detail, get_rankings, get_batsmen_rankings,
                         get_bowlers_rankings, get_allrounders_rankings, search_players,
                         get_player_info, get_player_batting_stats, get_player_bowling_stats,
                         get_recent_matches, get_match_details)
from .api_manager import CricketAPIManager
from .models import UserFavorite, APICallLog, CachedAPIResponse
from .team_stats import get_international_teams, get_team_stats, get_available_teams
import json
import io
import sys

def home(request):
    # Fetch cricket news
    news_items = get_cricket_news()
    context = {
        'news_items': news_items
    }
    return render(request, 'scores/home.html', context)

from django.shortcuts import render
from .cricbuzz_api import get_cricket_news

def news(request):
    news_items = get_cricket_news()
    context = {
        'news_items': news_items
    }
    return render(request, 'scores/news.html', context)

def player_search(request):
    query = request.GET.get('q', '')
    players = []
    if query:
        players = search_players(query)
    context = {
        'players': players,
        'query': query
    }
    return render(request, 'scores/player_search.html', context)

def news_detail(request, news_id):
    # Fetch detailed news article
    news = get_news_detail(news_id)
    if news is None:
        messages.error(request, 'Unable to fetch news article. Please try again later.')
        return redirect('home')
    context = {
        'news': news
    }
    return render(request, 'scores/news_detail.html', context)

def stats(request):
    # Get match type from request parameters
    match_type = request.GET.get('match_type', 'test')  # Default to test matches
    
    # Fetch team and player rankings for the selected format
    team_rankings = get_rankings(match_type)
    batsmen_rankings = get_batsmen_rankings(match_type)
    bowlers_rankings = get_bowlers_rankings(match_type)
    allrounders_rankings = get_allrounders_rankings(match_type)
    
    context = {
        'team_rankings': team_rankings,
        'batsmen_rankings': batsmen_rankings,
        'bowlers_rankings': bowlers_rankings,
        'allrounders_rankings': allrounders_rankings,
        'match_type': match_type,
        'match_types': [
            {'id': 'test', 'name': 'Test'},
            {'id': 'odi', 'name': 'ODI'},
            {'id': 't20', 'name': 'T20'}
        ]
    }
    
    return render(request, 'scores/stats.html', context)

from django.shortcuts import render
from .team_stats import get_international_teams

def stats_view(request):
    # Get team rankings
    team_rankings = get_international_teams()
    
    context = {
        'team_rankings': team_rankings,
        'batting_rankings': [],  # Placeholder for future implementation
        'bowling_rankings': [],  # Placeholder for future implementation
        'player_stats': []      # Placeholder for future implementation
    }
    return render(request, 'scores/stats.html', context)

def player_search(request):
    query = request.GET.get('q', '')
    players = []
    if query:
        players = search_players(query)
    context = {
        'query': query,
        'players': players
    }
    return render(request, 'scores/player_search.html', context)

def player_details(request, player_id):
    player_info = get_player_info(player_id)
    batting_stats = get_player_batting_stats(player_id)
    bowling_stats = get_player_bowling_stats(player_id)
    
    context = {
        'player_info': player_info,
        'batting_stats': batting_stats,
        'bowling_stats': bowling_stats
    }
    return render(request, 'scores/player_details.html', context)

def matches(request):
    # Fetch recent matches
    matches = get_recent_matches()
    context = {
        'matches': matches
    }
    return render(request, 'scores/matches.html', context)

def rankings(request):
    # Get match type from request parameters
    format_type = request.GET.get('format_type', 'test')  # Default to test matches
    
    # Fetch rankings data
    rankings = get_rankings(format_type)
    batsmen_rankings = get_batsmen_rankings(format_type)
    bowlers_rankings = get_bowlers_rankings(format_type)
    allrounders_rankings = get_allrounders_rankings(format_type)
    
    context = {
        'format_type': format_type,
        'rankings': rankings,  # Changed from team_rankings to rankings to match template
        'batsmen_rankings': batsmen_rankings,
        'bowlers_rankings': bowlers_rankings,
        'allrounders_rankings': allrounders_rankings
    }
    return render(request, 'scores/rankings.html', context)

def match_details(request, match_id):
    # Fetch match details
    match_data = get_match_details(match_id)
    if match_data is None:
        messages.error(request, 'Unable to fetch match details. Please try again later.')
        return redirect('matches')
    
    context = {
        'match_data': match_data,
        'venue': match_data.get('venue', {})
    }
    return render(request, 'scores/match_details.html', context)

def weather(request):
    # Placeholder for weather information
    context = {}
    return render(request, 'scores/weather.html', context)

def venues(request):
    # Placeholder for venues information
    context = {}
    return render(request, 'scores/venues.html', context)

def compare(request):
    # Placeholder for player comparison
    context = {}
    return render(request, 'scores/compare.html', context)

def photos(request):
    # Placeholder for cricket photos
    context = {}
    return render(request, 'scores/photos.html', context)

def api_stats(request):
    """Display API usage statistics"""
    total_calls = APICallLog.objects.count()
    successful_calls = APICallLog.objects.filter(success=True).count()
    failed_calls = APICallLog.objects.filter(success=False).count()
    
    # Recent API calls
    recent_calls = APICallLog.objects.order_by('-timestamp')[:20]
    
    # API calls by endpoint
    endpoint_stats = APICallLog.objects.values('endpoint').annotate(
        total=Count('id'),
        successful=Count('id', filter=models.Q(success=True)),
        avg_response_time=models.Avg('response_time')
    ).order_by('-total')[:10]
    
    context = {
        'total_calls': total_calls,
        'successful_calls': successful_calls,
        'failed_calls': failed_calls,
        'success_rate': (successful_calls / total_calls * 100) if total_calls > 0 else 0,
        'recent_calls': recent_calls,
        'endpoint_stats': endpoint_stats,
    }
    
    return render(request, 'scores/api_stats.html', context)

@staff_member_required
def cache_stats(request):
    """Display cache statistics and management interface"""
    total_cached = CachedAPIResponse.objects.count()
    active_cached = CachedAPIResponse.objects.filter(expires_at__gt=timezone.now()).count()
    expired_cached = CachedAPIResponse.objects.filter(expires_at__lte=timezone.now()).count()
    total_hits = CachedAPIResponse.objects.aggregate(total=Sum('hit_count'))['total'] or 0
    
    # Recent cache entries
    recent_cache = CachedAPIResponse.objects.order_by('-created_at')[:20]
    
    context = {
        'total_cached': total_cached,
        'active_cached': active_cached,
        'expired_cached': expired_cached,
        'total_hits': total_hits,
        'recent_cache': recent_cache,
    }
    
    return render(request, 'scores/cache_stats.html', context)

@staff_member_required
@require_POST
def refresh_cache_api(request):
    """API endpoint to refresh cache data"""
    try:
        data = json.loads(request.body) if request.body else {}
        force_refresh = data.get('force', False)
        
        # Capture command output
        output = io.StringIO()
        
        if force_refresh:
            call_command('refresh_cache', '--force-refresh', stdout=output)
            message = "All cache data has been force refreshed"
        else:
            call_command('refresh_cache', stdout=output)
            message = "Expired cache data has been refreshed"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'output': output.getvalue()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error refreshing cache: {str(e)}'
        })

@staff_member_required
@require_POST
def cleanup_cache_api(request):
    """API endpoint to cleanup expired cache"""
    try:
        # Capture command output
        output = io.StringIO()
        call_command('refresh_cache', '--cleanup-only', stdout=output)
        
        return JsonResponse({
            'success': True,
            'message': "Expired cache entries have been cleaned up",
            'output': output.getvalue()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error cleaning up cache: {str(e)}'
        })
