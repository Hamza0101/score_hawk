import requests
from django.core.cache import cache
from django.conf import settings
from .api_manager import CricketAPIManager
import logging

def get_cricket_news(user=None, ip_address=None):
    """Get cricket news using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/news/v1/index', force_cache=False)
    if data:
        return [item for item in data.get('storyList', []) if 'story' in item]
    return []

def get_news_detail(news_id, user=None, ip_address=None):
    """Get news detail using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    return api_manager.make_request(f'/news/v1/detail/{news_id}', force_cache=False)

def get_rankings(format_type='test', user=None, ip_address=None):
    """Get rankings using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/rankings/teams', {'formatType': format_type}, force_cache=False)
    if data:
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    return []

def get_batsmen_rankings(format_type='test', user=None, ip_address=None):
    """Get batsmen rankings using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/rankings/batsmen', {'formatType': format_type}, force_cache=False)
    if data:
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    return []

def get_bowlers_rankings(format_type='test', user=None, ip_address=None):
    """Get bowlers rankings using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/rankings/bowlers', {'formatType': format_type}, force_cache=False)
    if data:
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    return []

def get_allrounders_rankings(format_type='test', user=None, ip_address=None):
    """Get allrounders rankings using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/rankings/allrounders', {'formatType': format_type}, force_cache=False)
    if data:
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    return []

def search_players(player_name, user=None, ip_address=None):
    """Search players using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/stats/v1/player/search', {'plrN': player_name}, force_cache=False)
    if data:
        return data.get('player', [])
    return []

def get_player_info(player_id, user=None, ip_address=None):
    """Get player info using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    return api_manager.make_request(f'/stats/v1/player/{player_id}', force_cache=False)

def get_player_batting_stats(player_id, user=None, ip_address=None):
    """Get player batting stats using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request(f'/stats/v1/player/{player_id}/batting', force_cache=False)
    if data:
        formatted_stats = {}
        headers = data.get('headers', [])
        values = data.get('values', [])
        
        for format_index, format_type in enumerate(headers[1:], 1):
            stats = {}
            for stat_row in values:
                stat_name = stat_row['values'][0].lower()
                stat_value = stat_row['values'][format_index]
                
                if stat_name == 'matches':
                    stats['matches'] = stat_value
                elif stat_name == 'innings':
                    stats['innings'] = stat_value
                elif stat_name == 'runs':
                    stats['runs'] = stat_value
                elif stat_name == 'highest':
                    stats['highest'] = stat_value
                elif stat_name == 'average':
                    stats['average'] = stat_value
                elif stat_name == 'sr':
                    stats['strike_rate'] = stat_value
                elif stat_name == '100s':
                    stats['hundreds'] = stat_value
                elif stat_name == '50s':
                    stats['fifties'] = stat_value
                elif stat_name == 'fours':
                    stats['fours'] = stat_value
                elif stat_name == 'sixes':
                    stats['sixes'] = stat_value
            
            formatted_stats[format_type] = stats
        
        return formatted_stats
    return None

def get_player_bowling_stats(player_id, user=None, ip_address=None):
    """Get player bowling stats using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request(f'/stats/v1/player/{player_id}/bowling', force_cache=False)
    if data:
        formatted_stats = {}
        headers = data.get('headers', [])
        values = data.get('values', [])
        
        for format_index, format_type in enumerate(headers[1:], 1):
            stats = {}
            for stat_row in values:
                stat_name = stat_row['values'][0].lower()
                stat_value = stat_row['values'][format_index]
                
                if stat_name == 'matches':
                    stats['matches'] = stat_value
                elif stat_name == 'innings':
                    stats['innings'] = stat_value
                elif stat_name == 'balls':
                    stats['balls'] = stat_value
                elif stat_name == 'runs':
                    stats['runs'] = stat_value
                elif stat_name == 'maidens':
                    stats['maidens'] = stat_value
                elif stat_name == 'wickets':
                    stats['wickets'] = stat_value
                elif stat_name == 'avg':
                    stats['avg'] = stat_value
                elif stat_name == 'eco':
                    stats['eco'] = stat_value
                elif stat_name == 'sr':
                    stats['sr'] = stat_value
                elif stat_name == 'bbi':
                    stats['bbi'] = stat_value
                elif stat_name == 'bbm':
                    stats['bbm'] = stat_value
                elif stat_name == '4w':
                    stats['four_wickets'] = stat_value
                elif stat_name == '5w':
                    stats['five_wickets'] = stat_value
                elif stat_name == '10w':
                    stats['ten_wickets'] = stat_value
            
            formatted_stats[format_type] = stats
        
        return formatted_stats
    return None

def get_recent_matches(user=None, ip_address=None):
    """Get recent matches using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request('/matches/v1/recent', force_cache=False)
    if data:
        return data.get('typeMatches', [])
    return []

def get_match_details(match_id, user=None, ip_address=None):
    """Get match details using cached API manager"""
    api_manager = CricketAPIManager(user=user, ip_address=ip_address)
    data = api_manager.make_request(f'/mcenter/v1/{match_id}', force_cache=False)
    if data:
        
        # Extract match information
        match_info = {
            'match_id': data.get('matchInfo', {}).get('matchId'),
            'description': data.get('matchInfo', {}).get('matchDescription'),
            'format': data.get('matchInfo', {}).get('matchFormat'),
            'type': data.get('matchInfo', {}).get('matchType'),
            'status': data.get('matchInfo', {}).get('status'),
            'state': data.get('matchInfo', {}).get('state'),
            'start_time': data.get('matchInfo', {}).get('matchStartTimestamp'),
            'complete_time': data.get('matchInfo', {}).get('matchCompleteTimestamp'),
            'day_night': data.get('matchInfo', {}).get('dayNight'),
            'year': data.get('matchInfo', {}).get('year')
        }
        
        # Extract venue information
        venue_info = data.get('venueInfo', {})
        venue = {
            'name': venue_info.get('ground'),
            'city': venue_info.get('city'),
            'country': venue_info.get('country'),
            'capacity': venue_info.get('capacity'),
            'established': venue_info.get('established'),
            'known_as': venue_info.get('knownAs'),
            'ends': venue_info.get('ends'),
            'timezone': venue_info.get('timezone'),
            'home_team': venue_info.get('homeTeam'),
            'floodlights': venue_info.get('floodlights'),
            'curator': venue_info.get('curator'),
            'image_url': venue_info.get('imageUrl')
        }
        
        # Get leanback data for detailed match statistics
        leanback_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/leanback"
        leanback_data = api_manager.make_request('/mcenter/v1/{}/leanback'.format(match_id))
        
        if not leanback_data:
            return match_info
        
        # Extract miniscore information
        miniscore = leanback_data.get('miniscore', {})
        
        # Format current batting information
        current_batting = {
            'striker': {
                'id': miniscore.get('batsmanStriker', {}).get('batId', 0),
                'name': miniscore.get('batsmanStriker', {}).get('batName', ''),
                'runs': miniscore.get('batsmanStriker', {}).get('batRuns', 0),
                'balls': miniscore.get('batsmanStriker', {}).get('batBalls', 0),
                'dots': miniscore.get('batsmanStriker', {}).get('batDots', 0),
                'fours': miniscore.get('batsmanStriker', {}).get('batFours', 0),
                'sixes': miniscore.get('batsmanStriker', {}).get('batSixes', 0),
                'mins': miniscore.get('batsmanStriker', {}).get('batMins', 0),
                'strike_rate': miniscore.get('batsmanStriker', {}).get('batStrikeRate', 0.0)
            },
            'non_striker': {
                'id': miniscore.get('batsmanNonStriker', {}).get('batId', 0),
                'name': miniscore.get('batsmanNonStriker', {}).get('batName', ''),
                'runs': miniscore.get('batsmanNonStriker', {}).get('batRuns', 0),
                'balls': miniscore.get('batsmanNonStriker', {}).get('batBalls', 0),
                'dots': miniscore.get('batsmanNonStriker', {}).get('batDots', 0),
                'fours': miniscore.get('batsmanNonStriker', {}).get('batFours', 0),
                'sixes': miniscore.get('batsmanNonStriker', {}).get('batSixes', 0),
                'mins': miniscore.get('batsmanNonStriker', {}).get('batMins', 0),
                'strike_rate': miniscore.get('batsmanNonStriker', {}).get('batStrikeRate', 0.0)
            },
            'team_score': {
                'team_id': miniscore.get('batTeam', {}).get('teamId', 0),
                'team_name': miniscore.get('batTeam', {}).get('teamName', ''),
                'runs': miniscore.get('batTeam', {}).get('teamScore', 0),
                'wickets': miniscore.get('batTeam', {}).get('teamWkts', 0)
            },
            'current_partnership': {
                'runs': miniscore.get('partnerShip', {}).get('runs', 0),
                'balls': miniscore.get('partnerShip', {}).get('balls', 0)
            },
            'last_wicket': miniscore.get('lastWicket', ''),
            'last_wicket_score': miniscore.get('lastWicketScore', 0)
        }
        
        # Format current bowling information
        current_bowling = {
            'striker': {
                'id': miniscore.get('bowlerStriker', {}).get('bowlId', 0),
                'name': miniscore.get('bowlerStriker', {}).get('bowlName', ''),
                'overs': miniscore.get('bowlerStriker', {}).get('bowlOvs', 0),
                'maidens': miniscore.get('bowlerStriker', {}).get('bowlMaidens', 0),
                'runs': miniscore.get('bowlerStriker', {}).get('bowlRuns', 0),
                'wickets': miniscore.get('bowlerStriker', {}).get('bowlWkts', 0),
                'economy': miniscore.get('bowlerStriker', {}).get('bowlEcon', 0.0),
                'noballs': miniscore.get('bowlerStriker', {}).get('bowlNoballs', 0),
                'wides': miniscore.get('bowlerStriker', {}).get('bowlWides', 0)
            },
            'non_striker': {
                'id': miniscore.get('bowlerNonStriker', {}).get('bowlId', 0),
                'name': miniscore.get('bowlerNonStriker', {}).get('bowlName', ''),
                'overs': miniscore.get('bowlerNonStriker', {}).get('bowlOvs', 0),
                'maidens': miniscore.get('bowlerNonStriker', {}).get('bowlMaidens', 0),
                'runs': miniscore.get('bowlerNonStriker', {}).get('bowlRuns', 0),
                'wickets': miniscore.get('bowlerNonStriker', {}).get('bowlWkts', 0),
                'economy': miniscore.get('bowlerNonStriker', {}).get('bowlEcon', 0.0),
                'noballs': miniscore.get('bowlerNonStriker', {}).get('bowlNoballs', 0),
                'wides': miniscore.get('bowlerNonStriker', {}).get('bowlWides', 0)
            }
        }
        
        # Match progress information
        match_progress = {
            'innings_id': miniscore.get('inningsId', 0),
            'overs': miniscore.get('overs', 0.0),
            'current_run_rate': miniscore.get('currentRunRate', 0.0),
            'required_run_rate': miniscore.get('requiredRunRate', 0.0),
            'target': miniscore.get('target', 0),
            'recent_overs': miniscore.get('recentOvsStats', ''),
            'power_play': {
                'pp_1': miniscore.get('ppData', {}).get('pp_1', {})
            },
            'match_score_details': miniscore.get('matchScoreDetails', {}),
            'latest_performance': miniscore.get('latestPerformance', []),
            'over_summary_list': miniscore.get('overSummaryList', []),
            'rem_runs_to_win': miniscore.get('remRunsToWin', 0),
            'response_last_updated': miniscore.get('responseLastUpdated', 0)
        }
        
        return {
            'match_info': match_info,
            'venue': venue,
            'current_batting': current_batting,
            'current_bowling': current_bowling,
            'match_progress': match_progress
        }
    return None