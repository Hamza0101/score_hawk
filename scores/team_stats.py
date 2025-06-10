def get_international_teams(format_type='test', user=None, ip_address=None):
    from .api_manager import CricketAPIManager
    
    api_manager = CricketAPIManager()
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/teams"
    params = {
        'formatType': format_type
    }
    
    data = api_manager.make_request(url, params=params, user=user, ip_address=ip_address)
    
    teams = []
    if data and 'rank' in data:
        for team in data['rank']:
            teams.append({
                'rank': team.get('rank', 'N/A'),
                'team': team.get('name', 'Unknown'),
                'rating': team.get('rating', 'N/A')
            })
    
    return teams

def get_team_stats(team_id, match_type='test', user=None, ip_address=None):
    from .api_manager import CricketAPIManager
    
    api_manager = CricketAPIManager()
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/team/{team_id}"
    params = {
        'statsType': 'mostRuns',
        'matchType': match_type
    }

    data = api_manager.make_request(url, params=params, user=user, ip_address=ip_address)
    
    # Process the team statistics data
    stats = {
        'match_type': match_type,
        'team_id': team_id,
        'players': []
    }
    
    if data and 'values' in data:
        for player in data['values']:
            stats['players'].append({
                'name': player.get('name', ''),
                'runs': player.get('values', {}).get('runs', 0),
                'matches': player.get('values', {}).get('matches', 0),
                'average': player.get('values', {}).get('avg', 0.0),
                'strike_rate': player.get('values', {}).get('sr', 0.0),
                'highest_score': player.get('values', {}).get('hs', '0')
            })
    
    return stats

def get_available_teams():
    # This function returns the list of available teams with their IDs
    teams = [
        {'id': '2', 'name': 'India'},
        {'id': '3', 'name': 'Australia'},
        {'id': '4', 'name': 'England'},
        {'id': '5', 'name': 'South Africa'},
        {'id': '6', 'name': 'New Zealand'},
        {'id': '7', 'name': 'Pakistan'},
        {'id': '8', 'name': 'West Indies'},
        {'id': '9', 'name': 'Sri Lanka'},
        {'id': '10', 'name': 'Bangladesh'}
    ]
    return teams