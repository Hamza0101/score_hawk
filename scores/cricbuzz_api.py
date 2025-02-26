import requests

def get_cricket_news():
    url = "https://cricbuzz-cricket.p.rapidapi.com/news/v1/index"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        news_items = [item for item in data.get('storyList', []) if 'story' in item]
        return news_items
    except Exception as e:
        print(f"Error fetching cricket news: {e}")
        return []

def get_news_detail(news_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/news/v1/detail/{news_id}"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news detail: {e}")
        return None

def get_rankings(format_type='test'):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/teams"
    params = {
        'formatType': format_type
    }
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    except Exception as e:
        print(f"Error fetching rankings: {e}")
        return []

def get_batsmen_rankings(format_type='test'):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"
    params = {
        'formatType': format_type
    }
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    except Exception as e:
        print(f"Error fetching batsmen rankings: {e}")
        return []

def get_bowlers_rankings(format_type='test'):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/bowlers"
    params = {
        'formatType': format_type
    }
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    except Exception as e:
        print(f"Error fetching bowlers rankings: {e}")
        return []

def get_allrounders_rankings(format_type='test'):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/allrounders"
    params = {
        'formatType': format_type
    }
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rankings = [{
            'rank': player.get('rank'),
            'name': player.get('name'),
            'country': player.get('country'),
            'rating': player.get('rating')
        } for player in data.get('rank', [])]
        return rankings
    except Exception as e:
        print(f"Error fetching all-rounders rankings: {e}")
        return []

def search_players(player_name):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
    params = {
        'plrN': player_name
    }
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('player', [])
    except Exception as e:
        print(f"Error searching players: {e}")
        return []

def get_player_info(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching player info: {e}")
        return None

def get_player_batting_stats(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
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
    except Exception as e:
        print(f"Error fetching player batting stats: {e}")
        return None

def get_player_bowling_stats(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
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
    except Exception as e:
        print(f"Error fetching player bowling stats: {e}")
        return None

def get_recent_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('typeMatches', [])
    except Exception as e:
        print(f"Error fetching recent matches: {e}")
        return []

def get_match_details(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}"
    headers = {
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com',
        'x-rapidapi-key': '66ffd0f389mshca8c74e3d412ffap1b2f16jsn09bff14e9726'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
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
        leanback_response = requests.get(leanback_url, headers=headers)
        leanback_response.raise_for_status()
        leanback_data = leanback_response.json()
        
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
    except Exception as e:
        print(f"Error fetching match details: {e}")
        return None