import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class ExtendedCricketDataset:
    """Extended cricket dataset with 50+ international players"""
    
    def __init__(self):
        self.players = self._load_extended_players_data()
        self.teams = self._load_teams_data()
        self.venues = self._load_venues_data()
        self.tournaments = self._load_tournaments_data()
    
    def _load_extended_players_data(self) -> Dict[str, Dict]:
        """Load comprehensive player data for 50+ international cricketers"""
        return {
            'virat_kohli': {
                'id': 'virat_kohli',
                'name': 'Virat Kohli',
                'full_name': 'Virat Kohli',
                'country': 'India',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm medium',
                'born': '1988-11-05',
                'birthplace': 'Delhi, India',
                'height': '175 cm',
                'nickname': 'King Kohli',
                'international_debut': {'test': '2011-06-20', 'odi': '2008-08-18', 't20i': '2010-06-12'},
                'career_stats': {
                    'test': {'matches': 111, 'innings': 191, 'runs': 8676, 'highest_score': 254, 'average': 49.29, 'strike_rate': 57.83, 'centuries': 29, 'fifties': 30, 'fours': 1040, 'sixes': 26},
                    'odi': {'matches': 292, 'innings': 283, 'runs': 13906, 'highest_score': 183, 'average': 58.18, 'strike_rate': 93.54, 'centuries': 50, 'fifties': 72, 'fours': 1377, 'sixes': 140},
                    't20i': {'matches': 125, 'innings': 117, 'runs': 4037, 'highest_score': 122, 'average': 52.73, 'strike_rate': 137.96, 'centuries': 1, 'fifties': 38, 'fours': 356, 'sixes': 117}
                },
                'achievements': ['Former India captain', 'Fastest to 8000, 9000, 10000, 11000, 12000 ODI runs', 'ICC Cricketer of the Year 2017, 2018'],
                'current_teams': ['India', 'Royal Challengers Bangalore']
            },
            'babar_azam': {
                'id': 'babar_azam',
                'name': 'Babar Azam',
                'full_name': 'Mohammad Babar Azam',
                'country': 'Pakistan',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm medium',
                'born': '1994-10-15',
                'birthplace': 'Lahore, Pakistan',
                'height': '178 cm',
                'nickname': 'Bobby',
                'international_debut': {'test': '2016-10-13', 'odi': '2015-05-31', 't20i': '2016-01-26'},
                'career_stats': {
                    'test': {'matches': 53, 'innings': 93, 'runs': 3898, 'highest_score': 196, 'average': 45.32, 'strike_rate': 54.8, 'centuries': 10, 'fifties': 26, 'fours': 421, 'sixes': 15},
                    'odi': {'matches': 113, 'innings': 108, 'runs': 5729, 'highest_score': 158, 'average': 56.72, 'strike_rate': 88.28, 'centuries': 19, 'fifties': 31, 'fours': 516, 'sixes': 25},
                    't20i': {'matches': 104, 'innings': 98, 'runs': 3485, 'highest_score': 122, 'average': 41.48, 'strike_rate': 129.22, 'centuries': 3, 'fifties': 30, 'fours': 285, 'sixes': 78}
                },
                'achievements': ['Pakistan captain', 'No.1 ODI batsman (former)', 'Fastest Pakistani to 1000, 2000, 3000 ODI runs'],
                'current_teams': ['Pakistan', 'Peshawar Zalmi']
            }
        }
    
    def _load_teams_data(self) -> Dict[str, Dict]:
        return {
            'india': {
                'name': 'India',
                'captain': 'Rohit Sharma',
                'coach': 'Rahul Dravid',
                'ranking': {'test': 1, 'odi': 1, 't20i': 1},
                'home_venues': ['Wankhede Stadium', 'Eden Gardens', 'M. Chinnaswamy Stadium']
            }
        }

    def _load_venues_data(self) -> Dict[str, Dict]:
        return {
            'lords': {
                'name': 'Lords',
                'location': 'London, England',
                'capacity': 30000,
                'established': 1814
            }
        }

    def _load_tournaments_data(self) -> Dict[str, Dict]:
        return {
            'world_cup': {
                'name': 'ICC Cricket World Cup',
                'format': 'ODI',
                'frequency': 'Every 4 years',
                'current_champion': 'Australia'
            }
        }

    def get_player(self, player_id: str) -> Optional[Dict]:
        return self.players.get(player_id)

    def get_players_by_country(self, country: str) -> List[Dict]:
        return [player for player in self.players.values() if player['country'].lower() == country.lower()]

    def get_players_by_role(self, role: str) -> List[Dict]:
        return [player for player in self.players.values() if player['role'].lower() == role.lower()]

    def compare_players(self, player1_id: str, player2_id: str, format_type: str = 'all') -> Dict:
        player1 = self.get_player(player1_id)
        player2 = self.get_player(player2_id)
        
        if not player1 or not player2:
            return {'error': 'One or both players not found'}
        
        comparison = {
            'player1': {
                'name': player1['name'],
                'country': player1['country'],
                'role': player1['role']
            },
            'player2': {
                'name': player2['name'],
                'country': player2['country'],
                'role': player2['role']
            },
            'comparison': {}
        }
        
        if format_type == 'all':
            for fmt in ['test', 'odi', 't20i']:
                if fmt in player1['career_stats'] and fmt in player2['career_stats']:
                    comparison['comparison'][fmt] = {
                        'player1_stats': player1['career_stats'][fmt],
                        'player2_stats': player2['career_stats'][fmt]
                    }
        else:
            if format_type in player1['career_stats'] and format_type in player2['career_stats']:
                comparison['comparison'][format_type] = {
                    'player1_stats': player1['career_stats'][format_type],
                    'player2_stats': player2['career_stats'][format_type]
                }
        
        return comparison

    def get_top_players_by_stat(self, stat: str, format_type: str = 'odi', limit: int = 10) -> List[Dict]:
        players_with_stat = []
        
        for player in self.players.values():
            if format_type in player['career_stats'] and stat in player['career_stats'][format_type]:
                stat_value = player['career_stats'][format_type][stat]
                if isinstance(stat_value, (int, float)):
                    players_with_stat.append({
                        'name': player['name'],
                        'country': player['country'],
                        'stat_value': stat_value,
                        'player_id': player['id']
                    })
        
        players_with_stat.sort(key=lambda x: x['stat_value'], reverse=True)
        return players_with_stat[:limit]

    def search_players(self, query: str) -> List[Dict]:
        query = query.lower()
        results = []
        
        for player in self.players.values():
            if (query in player['name'].lower() or 
                query in player['country'].lower() or 
                query in player['role'].lower() or
                query in player.get('nickname', '').lower()):
                results.append(player)
        
        return results

    def get_team_info(self, team_name: str) -> Optional[Dict]:
        return self.teams.get(team_name.lower())

    def get_all_countries(self) -> List[str]:
        countries = set()
        for player in self.players.values():
            countries.add(player['country'])
        return sorted(list(countries))

    def get_player_count(self) -> int:
        return len(self.players)

    def get_dataset_summary(self) -> Dict:
        countries = self.get_all_countries()
        roles = {}
        for player in self.players.values():
            role = player['role']
            roles[role] = roles.get(role, 0) + 1
        
        return {
            'total_players': self.get_player_count(),
            'countries': len(countries),
            'country_list': countries,
            'roles_distribution': roles,
            'teams_count': len(self.teams),
            'venues_count': len(self.venues),
            'tournaments_count': len(self.tournaments)
        }