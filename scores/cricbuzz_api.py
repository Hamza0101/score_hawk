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