from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.management import call_command
from django.db.models import Sum, Count, Q, Avg
from django.db import models
import requests
from .cricbuzz_api import (get_cricket_news, get_news_detail, get_rankings, get_batsmen_rankings,
                         get_bowlers_rankings, get_allrounders_rankings, search_players,
                         get_player_info, get_player_batting_stats, get_player_bowling_stats,
                         get_recent_matches, get_match_details)
from .api_manager import CricketAPIManager
from .scorecard_manager import ScorecardManager
from .chatbot import CricketChatbot, ChatSession
from .models import (UserFavorite, APICallLog, CachedAPIResponse, UserSearchHistory,
                    ChatMessage, ChatSession as ChatSessionModel, UserPreference, MatchAlert, NewsBookmark)
from .team_stats import get_international_teams, get_team_stats, get_available_teams
import json
import io
import sys
import logging

logger = logging.getLogger(__name__)

def home(request):
    # Fetch cricket news with user context for better caching
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    # Fetch all data needed for home page
    news_items = get_cricket_news(user=user, ip_address=ip_address)
    team_rankings = get_rankings(user=user, ip_address=ip_address)
    batsmen_rankings = get_batsmen_rankings(user=user, ip_address=ip_address)
    bowlers_rankings = get_bowlers_rankings(user=user, ip_address=ip_address)
    
    context = {
        'news_items': news_items,
        'team_rankings': team_rankings,
        'batsmen_rankings': batsmen_rankings,
        'bowlers_rankings': bowlers_rankings
    }
    return render(request, 'scores/home.html', context)

from django.shortcuts import render
from .cricbuzz_api import get_cricket_news

def news(request):
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    news_items = get_cricket_news(user=user, ip_address=ip_address)
    context = {
        'news_items': news_items
    }
    return render(request, 'scores/news.html', context)

def player_search(request):
    query = request.GET.get('q', '')
    players = []
    if query:
        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR')
        players = search_players(query, user=user, ip_address=ip_address)
    context = {
        'players': players,
        'query': query
    }
    return render(request, 'scores/player_search.html', context)

def news_detail(request, news_id):
    # Fetch detailed news article with user context
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    news = get_news_detail(news_id, user=user, ip_address=ip_address)
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
    
    # Get user context for caching
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    # Fetch team and player rankings for the selected format
    team_rankings = get_rankings(match_type, user=user, ip_address=ip_address)
    batsmen_rankings = get_batsmen_rankings(match_type, user=user, ip_address=ip_address)
    bowlers_rankings = get_bowlers_rankings(match_type, user=user, ip_address=ip_address)
    allrounders_rankings = get_allrounders_rankings(match_type, user=user, ip_address=ip_address)
    
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
    # Get team rankings with user context
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    team_rankings = get_international_teams(user=user, ip_address=ip_address)
    
    context = {
        'team_rankings': team_rankings,
        'batting_rankings': [],  # Placeholder for future implementation
        'bowling_rankings': [],  # Placeholder for future implementation
        'player_stats': []      # Placeholder for future implementation
    }
    return render(request, 'scores/stats.html', context)

def player_details(request, player_id):
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    player_info = get_player_info(player_id, user=user, ip_address=ip_address)
    batting_stats = get_player_batting_stats(player_id, user=user, ip_address=ip_address)
    bowling_stats = get_player_bowling_stats(player_id, user=user, ip_address=ip_address)
    
    context = {
        'player_info': player_info,
        'batting_stats': batting_stats,
        'bowling_stats': bowling_stats
    }
    return render(request, 'scores/player_details.html', context)

def matches(request):
    # Fetch recent matches with user context
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    matches = get_recent_matches(user=user, ip_address=ip_address)
    context = {
        'matches': matches
    }
    return render(request, 'scores/matches.html', context)

def rankings(request):
    # Get match type from request parameters
    format_type = request.GET.get('format_type', 'test')  # Default to test matches
    
    # Get user context for caching
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    # Fetch rankings data
    rankings = get_rankings(format_type, user=user, ip_address=ip_address)
    batsmen_rankings = get_batsmen_rankings(format_type, user=user, ip_address=ip_address)
    bowlers_rankings = get_bowlers_rankings(format_type, user=user, ip_address=ip_address)
    allrounders_rankings = get_allrounders_rankings(format_type, user=user, ip_address=ip_address)
    
    context = {
        'format_type': format_type,
        'rankings': rankings,  # Changed from team_rankings to rankings to match template
        'batsmen_rankings': batsmen_rankings,
        'bowlers_rankings': bowlers_rankings,
        'allrounders_rankings': allrounders_rankings
    }
    return render(request, 'scores/rankings.html', context)

def match_details(request, match_id):
    # Fetch match details with user context
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    match_data = get_match_details(match_id, user=user, ip_address=ip_address)
    if match_data is None:
        messages.error(request, 'Unable to fetch match details. Please try again later.')
        return redirect('matches')
    
    context = {
        'match_data': match_data,
        'venue': match_data.get('venue', {})
    }
    return render(request, 'scores/match_details.html', context)

def enhanced_scorecard(request, match_id):
    """Enhanced scorecard view with detailed statistics"""
    user = request.user if request.user.is_authenticated else None
    scorecard_manager = ScorecardManager()
    
    try:
        scorecard_data = scorecard_manager.get_enhanced_scorecard(match_id, user=user)
        
        if scorecard_data.get('error'):
            messages.error(request, 'Unable to fetch scorecard details. Please try again later.')
            return redirect('matches')
        
        # Add live update capability for ongoing matches
        is_live = scorecard_data.get('match_status', {}).get('state') == 'Live'
        
        context = {
            'scorecard': scorecard_data,
            'match_id': match_id,
            'is_live': is_live,
            'auto_refresh': is_live  # Enable auto-refresh for live matches
        }
        
        return render(request, 'scores/enhanced_scorecard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading scorecard: {str(e)}')
        return redirect('matches')

@csrf_exempt
def scorecard_api(request, match_id):
    """API endpoint for scorecard data - used for live updates"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests allowed'}, status=405)
    
    try:
        user = request.user if request.user.is_authenticated else None
        scorecard_manager = ScorecardManager()
        
        scorecard_data = scorecard_manager.get_enhanced_scorecard(match_id, user=user)
        
        if scorecard_data.get('error'):
            return JsonResponse({
                'success': False,
                'error': 'Unable to fetch scorecard data'
            }, status=500)
        
        # Return simplified data structure for API
        api_response = {
            'success': True,
            'match_id': match_id,
            'status': scorecard_data.get('match_status', {}),
            'live_score': scorecard_data.get('live_score', {}),
            'current_innings': scorecard_data.get('current_innings', {}),
            'last_updated': timezone.now().isoformat()
        }
        
        return JsonResponse(api_response)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)

def live_commentary(request, match_id):
    """Get live commentary for a match"""
    user = request.user if request.user.is_authenticated else None
    scorecard_manager = ScorecardManager()
    
    try:
        commentary = scorecard_manager.get_live_commentary(match_id, user=user)
        
        return JsonResponse({
            'success': True,
            'commentary': commentary,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def add_favorite(request):
    """Add a team, player, or match to user favorites"""
    if request.method == 'POST':
        favorite_type = request.POST.get('type')  # 'team', 'player', 'match'
        favorite_id = request.POST.get('id')
        name = request.POST.get('name')
        
        favorite, created = UserFavorite.objects.get_or_create(
            user=request.user,
            favorite_type=favorite_type,
            favorite_id=favorite_id,
            defaults={'name': name}
        )
        
        if created:
            messages.success(request, f'{name} added to favorites!')
        else:
            messages.info(request, f'{name} is already in your favorites.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_favorite(request, favorite_id):
    """Remove a favorite"""
    favorite = get_object_or_404(UserFavorite, id=favorite_id, user=request.user)
    name = favorite.name
    favorite.delete()
    messages.success(request, f'{name} removed from favorites.')
    return redirect('user_favorites')

@login_required
def user_favorites(request):
    """Display user's favorites"""
    favorites = UserFavorite.objects.filter(user=request.user).order_by('-created_at')
    
    # Group favorites by type
    team_favorites = favorites.filter(favorite_type='team')
    player_favorites = favorites.filter(favorite_type='player')
    match_favorites = favorites.filter(favorite_type='match')
    
    context = {
        'team_favorites': team_favorites,
        'player_favorites': player_favorites,
        'match_favorites': match_favorites
    }
    
    return render(request, 'scores/user_favorites.html', context)

def search_with_history(request):
    """Enhanced search with history tracking"""
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'players')  # players, teams, matches
    
    if not query:
        return JsonResponse({'error': 'Search query required'}, status=400)
    
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    results = []
    results_count = 0
    
    try:
        if search_type == 'players':
            results = search_players(query, user=user, ip_address=ip_address)
            results_count = len(results) if results else 0
            
        # Save search history for authenticated users
        if user and user.is_authenticated:
            UserSearchHistory.objects.create(
                user=user,
                search_term=query,
                search_type=search_type,
                results_count=results_count
            )
        
        return JsonResponse({
            'success': True,
            'results': results,
            'count': results_count,
            'query': query,
            'type': search_type
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def search_history(request):
    """Display user's search history"""
    history = UserSearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:50]
    
    # Group by search type
    player_searches = history.filter(search_type='players')
    team_searches = history.filter(search_type='teams')
    match_searches = history.filter(search_type='matches')
    
    context = {
        'recent_searches': history[:10],
        'player_searches': player_searches[:10],
        'team_searches': team_searches[:10],
        'match_searches': match_searches[:10]
    }
    
    return render(request, 'scores/search_history.html', context)

def chatbot_interface(request):
    """Main chatbot interface page"""
    context = {
        'page_type': request.GET.get('page', 'general'),
        'match_id': request.GET.get('match_id'),
        'player_id': request.GET.get('player_id'),
    }
    return render(request, 'scores/chatbot.html', context)

@csrf_exempt
def chatbot_api(request):
    """API endpoint for chatbot interactions"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Get or create chat session
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key if not user else None
        
        chat_session = ChatSession(user=user, session_key=session_key)
        
        # Get response from chatbot
        start_time = timezone.now()
        response_data = chat_session.get_response(message, context=context)
        response_time = (timezone.now() - start_time).total_seconds()
        
        # Save message and response to database
        if user or session_key:
            # Save user message
            ChatMessage.objects.create(
                user=user,
                session_key=session_key,
                message=message,
                is_user=True,
                context_data=context
            )
            
            # Save bot response if successful
            if response_data.get('success'):
                ChatMessage.objects.create(
                    user=user,
                    session_key=session_key,
                    message=response_data['response'],
                    is_user=False,
                    context_data=context,
                    response_time=response_time,
                    tokens_used=response_data.get('tokens_used', 0)
                )
        
        # Get suggested questions for context
        suggested_questions = chat_session.get_suggested_questions(context)
        
        return JsonResponse({
            'success': True,
            'response': response_data['response'],
            'suggested_questions': suggested_questions,
            'response_time': response_time,
            'context': context
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error in chatbot API: {str(e)}")
        return JsonResponse({
            'error': 'Internal server error',
            'success': False
        }, status=500)

def quick_query_api(request):
    """API endpoint for quick queries (live scores, stats, etc.)"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests allowed'}, status=405)
    
    try:
        query_type = request.GET.get('type', '')
        
        if not query_type:
            return JsonResponse({'error': 'Query type is required'}, status=400)
        
        user = request.user if request.user.is_authenticated else None
        chatbot = CricketChatbot()
        
        params = dict(request.GET.items())
        response_data = chatbot.process_quick_query(query_type, params, user=user)
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in quick query API: {str(e)}")
        return JsonResponse({
            'error': 'Internal server error',
            'success': False
        }, status=500)

@login_required
def chat_history(request):
    """Display user's chat history"""
    messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:100]
    
    # Group messages by session/date
    grouped_messages = {}
    for message in messages:
        date_key = message.timestamp.date()
        if date_key not in grouped_messages:
            grouped_messages[date_key] = []
        grouped_messages[date_key].append(message)
    
    context = {
        'grouped_messages': grouped_messages,
        'total_messages': messages.count()
    }
    
    return render(request, 'scores/chat_history.html', context)

@login_required
def user_preferences(request):
    """User preferences page"""
    try:
        preferences = request.user.preferences
    except UserPreference.DoesNotExist:
        preferences = UserPreference.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        preferences.theme = request.POST.get('theme', 'light')
        preferences.notification_settings = request.POST.get('notifications', 'all')
        preferences.live_score_refresh_interval = int(request.POST.get('refresh_interval', 30))
        preferences.timezone = request.POST.get('timezone', 'UTC')
        preferences.email_notifications = request.POST.get('email_notifications') == 'on'
        preferences.push_notifications = request.POST.get('push_notifications') == 'on'
        preferences.save()
        
        messages.success(request, 'Preferences updated successfully!')
        return redirect('user_preferences')
    
    context = {
        'preferences': preferences
    }
    
    return render(request, 'scores/user_preferences.html', context)

@login_required
def bookmark_news(request):
    """Bookmark a news article"""
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        title = request.POST.get('title')
        url = request.POST.get('url', '')
        thumbnail = request.POST.get('thumbnail', '')
        
        bookmark, created = NewsBookmark.objects.get_or_create(
            user=request.user,
            news_id=news_id,
            defaults={
                'title': title,
                'url': url,
                'thumbnail': thumbnail
            }
        )
        
        if created:
            messages.success(request, 'News article bookmarked!')
        else:
            messages.info(request, 'Article is already bookmarked.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def bookmarked_news(request):
    """Display user's bookmarked news"""
    bookmarks = NewsBookmark.objects.filter(user=request.user)
    
    context = {
        'bookmarks': bookmarks
    }
    
    return render(request, 'scores/bookmarked_news.html', context)

@login_required
def create_match_alert(request):
    """Create alerts for match events"""
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        match_name = request.POST.get('match_name')
        alert_types = request.POST.getlist('alert_types')
        
        for alert_type in alert_types:
            MatchAlert.objects.get_or_create(
                user=request.user,
                match_id=match_id,
                alert_type=alert_type,
                defaults={'match_name': match_name}
            )
        
        messages.success(request, f'Alerts created for {match_name}!')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def user_alerts(request):
    """Display and manage user's match alerts"""
    active_alerts = MatchAlert.objects.filter(user=request.user, is_active=True)
    triggered_alerts = MatchAlert.objects.filter(user=request.user, is_active=False)[:20]
    
    context = {
        'active_alerts': active_alerts,
        'triggered_alerts': triggered_alerts
    }
    
    return render(request, 'scores/user_alerts.html', context)

def weather(request):
    # Placeholder for weather information
    context = {}
    return render(request, 'scores/weather.html', context)

def venues(request):
    # Placeholder for venues information
    context = {}
    return render(request, 'scores/venues.html', context)

def compare(request):
    """Enhanced player comparison view with real data integration"""
    player1_name = request.GET.get('player1', '')
    player2_name = request.GET.get('player2', '')
    player3_name = request.GET.get('player3', '')
    
    context = {
        'selected_players': {
            'player1': player1_name,
            'player2': player2_name,
            'player3': player3_name,
        }
    }
    
    # If players are selected, fetch their data
    if player1_name or player2_name:
        context['comparison_data'] = get_players_comparison_data([player1_name, player2_name, player3_name], request)
    
    return render(request, 'scores/compare.html', context)

def get_players_comparison_data(player_names, request):
    """Get comparison data for players with fallback to sample data"""
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    
    # Sample data for popular players when API data is insufficient
    sample_player_data = {
        'Virat Kohli': {
            'basic_info': {
                'name': 'Virat Kohli',
                'country': 'India',
                'role': 'Batsman',
                'playingRole': 'Top order Batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium',
                'id': '1413'
            },
            'details': {
                'DOB': '5 November 1988',
                'birthPlace': 'Delhi, India',
                'intlDebut': 'ODI: 18 August 2008 vs Sri Lanka',
                'teams': 'Royal Challengers Bangalore (IPL), India',
                'bio': 'Former Indian cricket team captain and one of the greatest batsmen of all time',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium'
            },
            'batting_stats': {
                'Test': {
                    'matches': '111', 'runs': '8676', 'average': '49.29', 'hundreds': '29', 'fifties': '30', 'highest': '254*'
                },
                'ODI': {
                    'matches': '295', 'runs': '13848', 'average': '58.18', 'hundreds': '50', 'fifties': '72', 'highest': '183'
                },
                'T20I': {
                    'matches': '125', 'runs': '4008', 'average': '52.73', 'hundreds': '1', 'fifties': '38', 'highest': '122*'
                }
            }
        },
        'Babar Azam': {
            'basic_info': {
                'name': 'Babar Azam',
                'country': 'Pakistan',
                'role': 'Batsman',
                'playingRole': 'Top order Batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium',
                'id': '4525'
            },
            'details': {
                'DOB': '15 October 1994',
                'birthPlace': 'Lahore, Pakistan',
                'intlDebut': 'ODI: 31 May 2015 vs Zimbabwe',
                'teams': 'Peshawar Zalmi (PSL), Pakistan',
                'bio': 'Current Pakistan cricket team captain and former No.1 ranked ODI and T20I batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium'
            },
            'batting_stats': {
                'Test': {
                    'matches': '54', 'runs': '3962', 'average': '45.30', 'hundreds': '10', 'fifties': '26', 'highest': '196'
                },
                'ODI': {
                    'matches': '113', 'runs': '5729', 'average': '59.05', 'hundreds': '19', 'fifties': '31', 'highest': '158'
                },
                'T20I': {
                    'matches': '104', 'runs': '3485', 'average': '41.48', 'hundreds': '3', 'fifties': '30', 'highest': '122'
                }
            }
        },
        'MS Dhoni': {
            'basic_info': {
                'name': 'MS Dhoni',
                'country': 'India',
                'role': 'Wicket-keeper',
                'playingRole': 'Wicket-keeper batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium',
                'id': '28'
            },
            'details': {
                'DOB': '7 July 1981',
                'birthPlace': 'Ranchi, India',
                'intlDebut': 'ODI: 23 December 2004 vs Bangladesh',
                'teams': 'Chennai Super Kings (IPL), Retired from International',
                'bio': 'Former Indian cricket team captain and 2011 World Cup winner',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm medium'
            },
            'batting_stats': {
                'Test': {
                    'matches': '90', 'runs': '4876', 'average': '38.09', 'hundreds': '6', 'fifties': '33', 'highest': '224'
                },
                'ODI': {
                    'matches': '350', 'runs': '10773', 'average': '50.57', 'hundreds': '10', 'fifties': '73', 'highest': '183*'
                },
                'T20I': {
                    'matches': '98', 'runs': '1617', 'average': '37.60', 'hundreds': '0', 'fifties': '2', 'highest': '56'
                }
            }
        },
        'Rohit Sharma': {
            'basic_info': {
                'name': 'Rohit Sharma',
                'country': 'India',
                'role': 'Batsman',
                'playingRole': 'Opening batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm off break',
                'id': '1076'
            },
            'details': {
                'DOB': '30 April 1987',
                'birthPlace': 'Nagpur, India',
                'intlDebut': 'ODI: 23 June 2007 vs Ireland',
                'teams': 'Mumbai Indians (IPL), India',
                'bio': 'Current Indian cricket team captain and prolific opening batsman',
                'battingStyle': 'Right-hand bat',
                'bowlingStyle': 'Right-arm off break'
            },
            'batting_stats': {
                'Test': {
                    'matches': '59', 'runs': '4301', 'average': '46.77', 'hundreds': '11', 'fifties': '21', 'highest': '212'
                },
                'ODI': {
                    'matches': '262', 'runs': '10866', 'average': '48.96', 'hundreds': '31', 'fifties': '56', 'highest': '264'
                },
                'T20I': {
                    'matches': '159', 'runs': '4231', 'average': '31.32', 'hundreds': '5', 'fifties': '32', 'highest': '118'
                }
            }
        },
        'David Warner': {
            'basic_info': {
                'name': 'David Warner',
                'country': 'Australia',
                'role': 'Batsman',
                'playingRole': 'Opening batsman',
                'battingStyle': 'Left-hand bat',
                'bowlingStyle': 'Right-arm leg break',
                'id': '5938'
            },
            'details': {
                'DOB': '27 October 1986',
                'birthPlace': 'Paddington, Australia',
                'intlDebut': 'ODI: 18 January 2009 vs South Africa',
                'teams': 'Sydney Thunder (BBL), Australia',
                'bio': 'Aggressive Australian opening batsman and former vice-captain',
                'battingStyle': 'Left-hand bat',
                'bowlingStyle': 'Right-arm leg break'
            },
            'batting_stats': {
                'Test': {
                    'matches': '112', 'runs': '8786', 'average': '44.59', 'hundreds': '26', 'fifties': '37', 'highest': '335*'
                },
                'ODI': {
                    'matches': '139', 'runs': '6007', 'average': '45.30', 'hundreds': '18', 'fifties': '33', 'highest': '179'
                },
                'T20I': {
                    'matches': '110', 'runs': '3277', 'average': '33.43', 'hundreds': '1', 'fifties': '28', 'highest': '100*'
                }
            }
        }
    }
    
    players_data = []
    for player_name in player_names:
        if not player_name.strip():
            continue
            
        # Try API first
        search_results = search_players(player_name, user=user, ip_address=ip_address)
        
        # Check if we have sample data for this player
        if player_name in sample_player_data:
            players_data.append(sample_player_data[player_name])
        elif search_results and len(search_results) > 0:
            player = search_results[0]
            # Get detailed player info if ID exists
            if 'id' in player:
                player_details = get_player_info(player['id'], user=user, ip_address=ip_address)
                batting_stats = get_player_batting_stats(player['id'], user=user, ip_address=ip_address)
                bowling_stats = get_player_bowling_stats(player['id'], user=user, ip_address=ip_address)
                
                players_data.append({
                    'basic_info': player,
                    'details': player_details,
                    'batting_stats': batting_stats,
                    'bowling_stats': bowling_stats,
                    'name': player_name
                })
            else:
                players_data.append({
                    'basic_info': player,
                    'details': None,
                    'batting_stats': None,
                    'bowling_stats': None,
                    'name': player_name
                })
        else:
            # Player not found, add placeholder
            players_data.append({
                'basic_info': {'name': player_name},
                'details': None,
                'batting_stats': None,
                'bowling_stats': None,
                'name': player_name
            })
    
    return players_data

@csrf_exempt
def compare_players_api(request):
    """API endpoint for player comparison data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        player_names = data.get('players', [])
        
        if not player_names or len(player_names) < 2:
            return JsonResponse({'error': 'At least 2 players required'}, status=400)
        
        # Use the improved function to get comparison data
        players_data = get_players_comparison_data(player_names, request)
        
        # Format for API response
        formatted_players = []
        for player_data in players_data:
            formatted_players.append({
                'name': player_data.get('basic_info', {}).get('name', 'Unknown'),
                'basic_info': player_data.get('basic_info'),
                'details': player_data.get('details'),
                'batting_stats': player_data.get('batting_stats'),
                'bowling_stats': player_data.get('bowling_stats'),
                'found': True if player_data.get('batting_stats') else False
            })
        
        return JsonResponse({
            'success': True,
            'players': formatted_players,
            'count': len(formatted_players)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Server error: {str(e)}',
            'success': False
        }, status=500)

@csrf_exempt 
def player_search_api(request):
    """API endpoint for player search suggestions - uses same logic as main player search"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests allowed'}, status=405)
    
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'players': []})
    
    try:
        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Use the same search function as the main player search page
        players = search_players(query, user=user, ip_address=ip_address)
        
        # Format response for frontend dropdown
        formatted_players = []
        if players:
            for player in players[:10]:  # Limit to 10 results
                formatted_players.append({
                    'id': player.get('id', ''),
                    'name': player.get('name', ''),
                    'team': player.get('teamName', player.get('team', '')),
                    'role': player.get('role', 'Player'),
                    'country': player.get('country', ''),
                    'ranking': player.get('ranking', None),
                    'dob': player.get('dob', ''),
                    'faceImageId': player.get('faceImageId', '')
                })
        
        return JsonResponse({
            'success': True,
            'players': formatted_players,
            'count': len(formatted_players)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Search error: {str(e)}',
            'success': False
        }, status=500)

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

def proxy_image(request, image_id):
    """Proxy view to serve images from RapidAPI with authentication"""
    try:
        # Construct the image URL
        image_url = f"https://cricbuzz-cricket.p.rapidapi.com/img/v1/i1/c{image_id}/i.jpg"
        
        # Headers for RapidAPI authentication
        headers = {
            'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
            'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
        }
        
        # Make the request to the external API
        response = requests.get(image_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Return the image with proper content type
            return HttpResponse(
                response.content,
                content_type='image/jpeg',
                headers={
                    'Cache-Control': 'public, max-age=86400',  # Cache for 24 hours
                    'Content-Length': len(response.content)
                }
            )
        else:
            # Return a placeholder or error response
            return HttpResponse(
                status=404,
                content="Image not found"
            )
            
    except Exception as e:
        # Return error response
        return HttpResponse(
            status=500,
            content=f"Error loading image: {str(e)}"
        )
