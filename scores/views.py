from django.shortcuts import render, redirect
from django.contrib import messages
from .cricbuzz_api import (get_cricket_news, get_news_detail, get_rankings, get_batsmen_rankings,
                         get_bowlers_rankings, get_allrounders_rankings, search_players,
                         get_player_info, get_player_batting_stats, get_player_bowling_stats)
from .team_stats import get_international_teams, get_team_stats, get_available_teams

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
