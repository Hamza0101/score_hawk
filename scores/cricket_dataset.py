import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class CricketDataset:
    """Comprehensive cricket dataset for chatbot and player comparisons"""
    
    def __init__(self):
        self.players = self._load_players_data()
        self.teams = self._load_teams_data()
        self.venues = self._load_venues_data()
        self.tournaments = self._load_tournaments_data()
        
    def _load_players_data(self) -> Dict[str, Dict]:
        """Load comprehensive player data"""
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
                'international_debut': {
                    'test': '2011-06-20',
                    'odi': '2008-08-18',
                    't20i': '2010-06-12'
                },
                'career_stats': {
                    'test': {
                        'matches': 113,
                        'innings': 193,
                        'runs': 8848,
                        'highest_score': 254,
                        'average': 49.15,
                        'strike_rate': 55.78,
                        'centuries': 29,
                        'fifties': 28,
                        'fours': 1040,
                        'sixes': 26,
                        'wickets': 1,
                        'bowling_average': 0.0
                    },
                    'odi': {
                        'matches': 295,
                        'innings': 283,
                        'runs': 13906,
                        'highest_score': 183,
                        'average': 58.18,
                        'strike_rate': 93.54,
                        'centuries': 50,
                        'fifties': 72,
                        'fours': 1377,
                        'sixes': 124,
                        'wickets': 4,
                        'bowling_average': 166.25
                    },
                    't20i': {
                        'matches': 125,
                        'innings': 117,
                        'runs': 4188,
                        'highest_score': 122,
                        'average': 48.69,
                        'strike_rate': 137.04,
                        'centuries': 1,
                        'fifties': 38,
                        'fours': 356,
                        'sixes': 117,
                        'wickets': 4,
                        'bowling_average': 7.25
                    }
                },
                'achievements': [
                    'ICC Cricketer of the Year 2017, 2018',
                    'Wisden Leading Cricketer 2016, 2017, 2018',
                    'Former India captain (2017-2022)',
                    'Fastest to 8000, 9000, 10000, 11000, 12000 ODI runs',
                    'Most runs in T20I cricket',
                    'Most centuries in successful ODI chases'
                ],
                'current_teams': ['India', 'Royal Challengers Bangalore'],
                'ipl_stats': {
                    'matches': 237,
                    'runs': 7263,
                    'average': 36.32,
                    'strike_rate': 130.41,
                    'centuries': 7,
                    'fifties': 50
                }
            },
            'babar_azam': {
                'id': 'babar_azam',
                'name': 'Babar Azam',
                'full_name': 'Babar Azam',
                'country': 'Pakistan',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm off break',
                'born': '1994-10-15',
                'birthplace': 'Lahore, Pakistan',
                'height': '180 cm',
                'nickname': 'Bobby',
                'international_debut': {
                    'test': '2016-10-13',
                    'odi': '2015-05-31',
                    't20i': '2016-01-26'
                },
                'career_stats': {
                    'test': {
                        'matches': 53,
                        'innings': 89,
                        'runs': 3898,
                        'highest_score': 196,
                        'average': 45.32,
                        'strike_rate': 54.71,
                        'centuries': 10,
                        'fifties': 26,
                        'fours': 421,
                        'sixes': 15,
                        'wickets': 0,
                        'bowling_average': 0.0
                    },
                    'odi': {
                        'matches': 117,
                        'innings': 114,
                        'runs': 5729,
                        'highest_score': 158,
                        'average': 56.72,
                        'strike_rate': 88.28,
                        'centuries': 19,
                        'fifties': 31,
                        'fours': 559,
                        'sixes': 25,
                        'wickets': 0,
                        'bowling_average': 0.0
                    },
                    't20i': {
                        'matches': 122,
                        'innings': 115,
                        'runs': 4192,
                        'highest_score': 122,
                        'average': 41.50,
                        'strike_rate': 128.40,
                        'centuries': 3,
                        'fifties': 33,
                        'fours': 358,
                        'sixes': 78,
                        'wickets': 0,
                        'bowling_average': 0.0
                    }
                },
                'achievements': [
                    'Pakistan captain (2019-present)',
                    'No.1 ranked ODI batsman (2021-2023)',
                    'No.1 ranked T20I batsman (2021-2022)',
                    'Youngest to score 3000 T20I runs',
                    'First Pakistani to score centuries in first 4 Tests as captain'
                ],
                'current_teams': ['Pakistan', 'Peshawar Zalmi'],
                'psl_stats': {
                    'matches': 78,
                    'runs': 2413,
                    'average': 35.48,
                    'strike_rate': 125.84,
                    'centuries': 1,
                    'fifties': 19
                }
            },
            'steve_smith': {
                'id': 'steve_smith',
                'name': 'Steve Smith',
                'full_name': 'Steven Peter Devereux Smith',
                'country': 'Australia',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm leg break',
                'born': '1989-06-02',
                'birthplace': 'Sydney, Australia',
                'height': '175 cm',
                'nickname': 'Smudge',
                'international_debut': {
                    'test': '2010-07-13',
                    'odi': '2010-02-19',
                    't20i': '2010-02-17'
                },
                'career_stats': {
                    'test': {
                        'matches': 109,
                        'innings': 193,
                        'runs': 9685,
                        'highest_score': 239,
                        'average': 56.97,
                        'strike_rate': 54.36,
                        'centuries': 32,
                        'fifties': 41,
                        'fours': 1089,
                        'sixes': 28,
                        'wickets': 17,
                        'bowling_average': 54.94
                    },
                    'odi': {
                        'matches': 155,
                        'innings': 142,
                        'runs': 4939,
                        'highest_score': 164,
                        'average': 43.34,
                        'strike_rate': 87.86,
                        'centuries': 12,
                        'fifties': 28,
                        'fours': 456,
                        'sixes': 37,
                        'wickets': 29,
                        'bowling_average': 51.55
                    },
                    't20i': {
                        'matches': 67,
                        'innings': 58,
                        'runs': 1216,
                        'highest_score': 83,
                        'average': 26.43,
                        'strike_rate': 126.03,
                        'centuries': 0,
                        'fifties': 6,
                        'fours': 95,
                        'sixes': 24,
                        'wickets': 17,
                        'bowling_average': 31.76
                    }
                },
                'achievements': [
                    'Former Australia captain (2015-2018)',
                    'ICC Test Player of the Decade (2011-2020)',
                    'Allan Border Medal winner (2015, 2018, 2021)',
                    'Fastest Australian to 7000 Test runs',
                    'Most runs in 2019 Ashes series (774 runs)'
                ],
                'current_teams': ['Australia', 'Sydney Sixers'],
                'ipl_stats': {
                    'matches': 103,
                    'runs': 2333,
                    'average': 26.74,
                    'strike_rate': 128.11,
                    'centuries': 1,
                    'fifties': 13
                }
            },
            'rohit_sharma': {
                'id': 'rohit_sharma',
                'name': 'Rohit Sharma',
                'full_name': 'Rohit Gurunath Sharma',
                'country': 'India',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm off break',
                'born': '1987-04-30',
                'birthplace': 'Nagpur, India',
                'height': '173 cm',
                'nickname': 'Hitman',
                'international_debut': {
                    'test': '2013-11-06',
                    'odi': '2007-06-23',
                    't20i': '2007-09-19'
                },
                'career_stats': {
                    'test': {
                        'matches': 67,
                        'innings': 116,
                        'runs': 4301,
                        'highest_score': 212,
                        'average': 42.58,
                        'strike_rate': 55.69,
                        'centuries': 11,
                        'fifties': 16,
                        'fours': 456,
                        'sixes': 69,
                        'wickets': 2,
                        'bowling_average': 27.00
                    },
                    'odi': {
                        'matches': 265,
                        'innings': 255,
                        'runs': 10866,
                        'highest_score': 264,
                        'average': 48.96,
                        'strike_rate': 90.99,
                        'centuries': 31,
                        'fifties': 56,
                        'fours': 1018,
                        'sixes': 298,
                        'wickets': 8,
                        'bowling_average': 61.62
                    },
                    't20i': {
                        'matches': 159,
                        'innings': 151,
                        'runs': 4231,
                        'highest_score': 121,
                        'average': 31.32,
                        'strike_rate': 139.24,
                        'centuries': 5,
                        'fifties': 31,
                        'fours': 335,
                        'sixes': 190,
                        'wickets': 2,
                        'bowling_average': 8.00
                    }
                },
                'achievements': [
                    'Current India captain (2022-present)',
                    'Only player with 3 ODI double centuries',
                    'Most sixes in ODI cricket (298+)',
                    'Most centuries in T20I cricket (5)',
                    'IPL winner as captain (2013, 2015, 2017, 2019, 2020)'
                ],
                'current_teams': ['India', 'Mumbai Indians'],
                'ipl_stats': {
                    'matches': 257,
                    'runs': 6628,
                    'average': 30.32,
                    'strike_rate': 130.61,
                    'centuries': 2,
                    'fifties': 42
                }
            },
            'kane_williamson': {
                'id': 'kane_williamson',
                'name': 'Kane Williamson',
                'full_name': 'Kane Stuart Williamson',
                'country': 'New Zealand',
                'role': 'Batsman',
                'batting_style': 'Right-hand bat',
                'bowling_style': 'Right-arm off break',
                'born': '1990-08-08',
                'birthplace': 'Tauranga, New Zealand',
                'height': '180 cm',
                'nickname': 'Captain Cool',
                'international_debut': {
                    'test': '2010-11-04',
                    'odi': '2010-08-14',
                    't20i': '2011-02-25'
                },
                'career_stats': {
                    'test': {
                        'matches': 101,
                        'innings': 183,
                        'runs': 8743,
                        'highest_score': 251,
                        'average': 54.31,
                        'strike_rate': 51.93,
                        'centuries': 32,
                        'fifties': 35,
                        'fours': 1002,
                        'sixes': 21,
                        'wickets': 2,
                        'bowling_average': 34.50
                    },
                    'odi': {
                        'matches': 167,
                        'innings': 159,
                        'runs': 6173,
                        'highest_score': 148,
                        'average': 47.48,
                        'strike_rate': 81.54,
                        'centuries': 13,
                        'fifties': 42,
                        'fours': 548,
                        'sixes': 37,
                        'wickets': 37,
                        'bowling_average': 41.43
                    },
                    't20i': {
                        'matches': 93,
                        'innings': 85,
                        'runs': 2021,
                        'highest_score': 95,
                        'average': 27.28,
                        'strike_rate': 123.17,
                        'centuries': 0,
                        'fifties': 11,
                        'fours': 166,
                        'sixes': 36,
                        'wickets': 4,
                        'bowling_average': 36.25
                    }
                },
                'achievements': [
                    'New Zealand captain (2016-present)',
                    'ICC Test Player of the Year 2021',
                    'World Test Championship winner 2021',
                    'CWC 2019 finalist',
                    'Youngest New Zealand captain'
                ],
                'current_teams': ['New Zealand', 'Sunrisers Hyderabad'],
                'ipl_stats': {
                    'matches': 79,
                    'runs': 2101,
                    'average': 34.43,
                    'strike_rate': 123.96,
                    'centuries': 1,
                    'fifties': 13
                }
            }
        }
    
    def _load_teams_data(self) -> Dict[str, Dict]:
        """Load comprehensive team data"""
        return {
            'india': {
                'id': 'india',
                'name': 'India',
                'full_name': 'India National Cricket Team',
                'captain': {
                    'test': 'Rohit Sharma',
                    'odi': 'Rohit Sharma',
                    't20i': 'Rohit Sharma'
                },
                'coach': 'Rahul Dravid',
                'founded': 1932,
                'home_ground': 'Various',
                'major_achievements': {
                    'world_cups': {
                        'odi': [1983, 2011],
                        't20': [2007, 2024]
                    },
                    'champions_trophy': [2002, 2013],
                    'world_test_championship': [2021]
                },
                'icc_rankings': {
                    'test': 1,
                    'odi': 1,
                    't20i': 1
                },
                'colors': ['Blue', 'Orange'],
                'nickname': 'Men in Blue'
            },
            'australia': {
                'id': 'australia',
                'name': 'Australia',
                'full_name': 'Australia National Cricket Team',
                'captain': {
                    'test': 'Pat Cummins',
                    'odi': 'Pat Cummins',
                    't20i': 'Mitchell Marsh'
                },
                'coach': 'Andrew McDonald',
                'founded': 1877,
                'home_ground': 'Various',
                'major_achievements': {
                    'world_cups': {
                        'odi': [1987, 1999, 2003, 2007, 2015, 2023],
                        't20': [2021]
                    },
                    'champions_trophy': [2006, 2009],
                    'world_test_championship': [2023]
                },
                'icc_rankings': {
                    'test': 2,
                    'odi': 2,
                    't20i': 3
                },
                'colors': ['Yellow', 'Green'],
                'nickname': 'Aussies'
            },
            'england': {
                'id': 'england',
                'name': 'England',
                'full_name': 'England Cricket Team',
                'captain': {
                    'test': 'Ben Stokes',
                    'odi': 'Jos Buttler',
                    't20i': 'Jos Buttler'
                },
                'coach': 'Brendon McCullum',
                'founded': 1877,
                'home_ground': 'Lord\'s Cricket Ground',
                'major_achievements': {
                    'world_cups': {
                        'odi': [2019],
                        't20': [2010, 2022]
                    },
                    'champions_trophy': [2004, 2017]
                },
                'icc_rankings': {
                    'test': 4,
                    'odi': 4,
                    't20i': 2
                },
                'colors': ['Blue', 'Red'],
                'nickname': 'Three Lions'
            },
            'pakistan': {
                'id': 'pakistan',
                'name': 'Pakistan',
                'full_name': 'Pakistan National Cricket Team',
                'captain': {
                    'test': 'Shan Masood',
                    'odi': 'Babar Azam',
                    't20i': 'Babar Azam'
                },
                'coach': 'Gary Kirsten',
                'founded': 1952,
                'home_ground': 'Various',
                'major_achievements': {
                    'world_cups': {
                        'odi': [1992],
                        't20': [2009]
                    },
                    'champions_trophy': [2017]
                },
                'icc_rankings': {
                    'test': 8,
                    'odi': 5,
                    't20i': 4
                },
                'colors': ['Green', 'White'],
                'nickname': 'Shaheens'
            },
            'new_zealand': {
                'id': 'new_zealand',
                'name': 'New Zealand',
                'full_name': 'New Zealand National Cricket Team',
                'captain': {
                    'test': 'Tim Southee',
                    'odi': 'Kane Williamson',
                    't20i': 'Kane Williamson'
                },
                'coach': 'Gary Stead',
                'founded': 1930,
                'home_ground': 'Various',
                'major_achievements': {
                    'world_cups': {
                        'odi': [],
                        't20': []
                    },
                    'world_test_championship': [2021]
                },
                'icc_rankings': {
                    'test': 3,
                    'odi': 6,
                    't20i': 5
                },
                'colors': ['Black'],
                'nickname': 'Black Caps'
            }
        }
    
    def _load_venues_data(self) -> Dict[str, Dict]:
        """Load venue data"""
        return {
            'lords': {
                'id': 'lords',
                'name': 'Lord\'s Cricket Ground',
                'city': 'London',
                'country': 'England',
                'capacity': 31100,
                'established': 1814,
                'nickname': 'Home of Cricket',
                'notable_matches': [
                    '2019 Cricket World Cup Final',
                    '1975 Cricket World Cup Final'
                ]
            },
            'mcg': {
                'id': 'mcg',
                'name': 'Melbourne Cricket Ground',
                'city': 'Melbourne',
                'country': 'Australia',
                'capacity': 100024,
                'established': 1853,
                'nickname': 'The G',
                'notable_matches': [
                    '2015 Cricket World Cup Final',
                    'Boxing Day Tests'
                ]
            },
            'eden_gardens': {
                'id': 'eden_gardens',
                'name': 'Eden Gardens',
                'city': 'Kolkata',
                'country': 'India',
                'capacity': 66000,
                'established': 1864,
                'nickname': 'Cricket\'s Colosseum',
                'notable_matches': [
                    '1987 Cricket World Cup Final',
                    '2016 T20 World Cup Final'
                ]
            }
        }
    
    def _load_tournaments_data(self) -> Dict[str, Dict]:
        """Load tournament data"""
        return {
            'cricket_world_cup': {
                'id': 'cricket_world_cup',
                'name': 'ICC Cricket World Cup',
                'format': 'ODI',
                'frequency': 4,  # years
                'first_edition': 1975,
                'current_champion': 'Australia',
                'most_titles': 'Australia (6 titles)'
            },
            't20_world_cup': {
                'id': 't20_world_cup',
                'name': 'ICC T20 World Cup',
                'format': 'T20I',
                'frequency': 2,  # years
                'first_edition': 2007,
                'current_champion': 'India',
                'most_titles': 'West Indies (2 titles)'
            },
            'champions_trophy': {
                'id': 'champions_trophy',
                'name': 'ICC Champions Trophy',
                'format': 'ODI',
                'frequency': 4,  # years
                'first_edition': 1998,
                'current_champion': 'Pakistan',
                'most_titles': 'Australia, India (2 titles each)'
            },
            'world_test_championship': {
                'id': 'world_test_championship',
                'name': 'ICC World Test Championship',
                'format': 'Test',
                'frequency': 2,  # years
                'first_edition': 2019,
                'current_champion': 'Australia',
                'most_titles': 'New Zealand, Australia (1 title each)'
            }
        }
    
    def get_player(self, player_id: str) -> Optional[Dict]:
        """Get player data by ID"""
        return self.players.get(player_id.lower().replace(' ', '_'))
    
    def search_players(self, query: str) -> List[Dict]:
        """Search players by name"""
        query = query.lower()
        results = []
        for player_id, player_data in self.players.items():
            if (query in player_data['name'].lower() or 
                query in player_data['full_name'].lower() or
                query in player_data.get('nickname', '').lower()):
                results.append(player_data)
        return results
    
    def get_team(self, team_id: str) -> Optional[Dict]:
        """Get team data by ID"""
        return self.teams.get(team_id.lower())
    
    def compare_players(self, player1_id: str, player2_id: str, format_type: str = 'all') -> Dict:
        """Compare two players across different formats"""
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
        
        formats = ['test', 'odi', 't20i'] if format_type == 'all' else [format_type]
        
        for fmt in formats:
            if fmt in player1['career_stats'] and fmt in player2['career_stats']:
                p1_stats = player1['career_stats'][fmt]
                p2_stats = player2['career_stats'][fmt]
                
                comparison['comparison'][fmt] = {
                    'matches': {
                        'player1': p1_stats.get('matches', 0),
                        'player2': p2_stats.get('matches', 0),
                        'winner': 'player1' if p1_stats.get('matches', 0) > p2_stats.get('matches', 0) else 'player2'
                    },
                    'runs': {
                        'player1': p1_stats.get('runs', 0),
                        'player2': p2_stats.get('runs', 0),
                        'winner': 'player1' if p1_stats.get('runs', 0) > p2_stats.get('runs', 0) else 'player2'
                    },
                    'average': {
                        'player1': p1_stats.get('average', 0),
                        'player2': p2_stats.get('average', 0),
                        'winner': 'player1' if p1_stats.get('average', 0) > p2_stats.get('average', 0) else 'player2'
                    },
                    'strike_rate': {
                        'player1': p1_stats.get('strike_rate', 0),
                        'player2': p2_stats.get('strike_rate', 0),
                        'winner': 'player1' if p1_stats.get('strike_rate', 0) > p2_stats.get('strike_rate', 0) else 'player2'
                    },
                    'centuries': {
                        'player1': p1_stats.get('centuries', 0),
                        'player2': p2_stats.get('centuries', 0),
                        'winner': 'player1' if p1_stats.get('centuries', 0) > p2_stats.get('centuries', 0) else 'player2'
                    },
                    'fifties': {
                        'player1': p1_stats.get('fifties', 0),
                        'player2': p2_stats.get('fifties', 0),
                        'winner': 'player1' if p1_stats.get('fifties', 0) > p2_stats.get('fifties', 0) else 'player2'
                    }
                }
        
        return comparison
    
    def get_top_players_by_stat(self, stat: str, format_type: str = 'odi', limit: int = 5) -> List[Dict]:
        """Get top players by a specific statistic"""
        players_with_stat = []
        
        for player_id, player_data in self.players.items():
            if format_type in player_data['career_stats']:
                stat_value = player_data['career_stats'][format_type].get(stat, 0)
                players_with_stat.append({
                    'name': player_data['name'],
                    'country': player_data['country'],
                    'value': stat_value,
                    'player_id': player_id
                })
        
        # Sort by stat value in descending order
        players_with_stat.sort(key=lambda x: x['value'], reverse=True)
        
        return players_with_stat[:limit]
    
    def get_player_achievements(self, player_id: str) -> List[str]:
        """Get player achievements"""
        player = self.get_player(player_id)
        return player.get('achievements', []) if player else []
    
    def get_format_leaders(self) -> Dict:
        """Get format leaders in key statistics"""
        return {
            'test': {
                'most_runs': self.get_top_players_by_stat('runs', 'test', 1)[0] if self.get_top_players_by_stat('runs', 'test', 1) else None,
                'highest_average': self.get_top_players_by_stat('average', 'test', 1)[0] if self.get_top_players_by_stat('average', 'test', 1) else None,
                'most_centuries': self.get_top_players_by_stat('centuries', 'test', 1)[0] if self.get_top_players_by_stat('centuries', 'test', 1) else None
            },
            'odi': {
                'most_runs': self.get_top_players_by_stat('runs', 'odi', 1)[0] if self.get_top_players_by_stat('runs', 'odi', 1) else None,
                'highest_average': self.get_top_players_by_stat('average', 'odi', 1)[0] if self.get_top_players_by_stat('average', 'odi', 1) else None,
                'most_centuries': self.get_top_players_by_stat('centuries', 'odi', 1)[0] if self.get_top_players_by_stat('centuries', 'odi', 1) else None
            },
            't20i': {
                'most_runs': self.get_top_players_by_stat('runs', 't20i', 1)[0] if self.get_top_players_by_stat('runs', 't20i', 1) else None,
                'highest_average': self.get_top_players_by_stat('average', 't20i', 1)[0] if self.get_top_players_by_stat('average', 't20i', 1) else None,
                'highest_strike_rate': self.get_top_players_by_stat('strike_rate', 't20i', 1)[0] if self.get_top_players_by_stat('strike_rate', 't20i', 1) else None
            }
        }

# Global instance
cricket_dataset = CricketDataset()