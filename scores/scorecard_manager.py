import json
import logging
from typing import Dict, List, Any, Optional
from .api_manager import CricketAPIManager

logger = logging.getLogger(__name__)

class ScorecardManager:
    """Enhanced scorecard manager with better data processing"""
    
    def __init__(self):
        self.api_manager = CricketAPIManager()
    
    def get_enhanced_scorecard(self, match_id: str, user=None) -> Dict[str, Any]:
        """Get enhanced scorecard data with proper error handling"""
        try:
            # Get match details from API
            match_data = self.api_manager.make_request(
                f'/mcenter/v1/{match_id}', 
                user=user
            )
            
            if not match_data:
                return self._get_empty_scorecard()
            
            return self._process_scorecard_data(match_data, match_id)
            
        except Exception as e:
            logger.error(f"Error getting enhanced scorecard for match {match_id}: {str(e)}")
            return self._get_empty_scorecard()
    
    def _process_scorecard_data(self, raw_data: Dict, match_id: str) -> Dict[str, Any]:
        """Process and structure scorecard data"""
        processed_data = {
            'match_id': match_id,
            'match_info': self._extract_match_info(raw_data),
            'teams': self._extract_teams(raw_data),
            'innings': self._extract_innings(raw_data),
            'live_score': self._extract_live_score(raw_data),
            'match_status': self._extract_match_status(raw_data),
            'venue': self._extract_venue(raw_data),
            'officials': self._extract_officials(raw_data),
            'weather': self._extract_weather(raw_data),
            'toss': self._extract_toss(raw_data),
            'series_info': self._extract_series_info(raw_data)
        }
        
        return processed_data
    
    def _extract_match_info(self, data: Dict) -> Dict[str, Any]:
        """Extract basic match information"""
        match_header = data.get('matchHeader', {})
        match_info = match_header.get('matchInfo', {})
        
        return {
            'match_id': match_info.get('matchId'),
            'match_format': match_info.get('matchFormat'),
            'match_type': match_info.get('matchType'),
            'complete_datetime': match_info.get('completeDateTime'),
            'current_gmtoffset': match_info.get('currentGmtOffset'),
            'is_day_night': match_info.get('isDayNight', False),
            'state': match_header.get('state'),
            'status': match_header.get('status'),
            'play_status': match_header.get('playStatus'),
            'result': match_header.get('result'),
            'revision_number': match_header.get('revisedTarget', {}).get('reason') if match_header.get('revisedTarget') else None
        }
    
    def _extract_teams(self, data: Dict) -> Dict[str, Any]:
        """Extract team information"""
        match_header = data.get('matchHeader', {})
        team1 = match_header.get('team1', {})
        team2 = match_header.get('team2', {})
        
        return {
            'team1': {
                'id': team1.get('id'),
                'name': team1.get('name'),
                'short_name': team1.get('shortName'),
                'logo_url': team1.get('imageUrl'),
                'players_count': team1.get('playersCount', 11)
            },
            'team2': {
                'id': team2.get('id'),
                'name': team2.get('name'),
                'short_name': team2.get('shortName'),
                'logo_url': team2.get('imageUrl'),
                'players_count': team2.get('playersCount', 11)
            }
        }
    
    def _extract_innings(self, data: Dict) -> List[Dict[str, Any]]:
        """Extract innings data with batting and bowling stats"""
        scorecard_data = data.get('scoreCard', [])
        innings_list = []
        
        for innings_data in scorecard_data:
            innings_info = {
                'innings_id': innings_data.get('inningsId'),
                'batting_team_id': innings_data.get('batTeamDetails', {}).get('batTeamId'),
                'batting_team_name': innings_data.get('batTeamDetails', {}).get('batTeamName'),
                'batting_team_short_name': innings_data.get('batTeamDetails', {}).get('batTeamShortName'),
                'bowling_team_id': innings_data.get('bowlTeamDetails', {}).get('bowlTeamId'),
                'bowling_team_name': innings_data.get('bowlTeamDetails', {}).get('bowlTeamName'),
                'bowling_team_short_name': innings_data.get('bowlTeamDetails', {}).get('bowlTeamShortName'),
                'score_details': self._process_score_details(innings_data.get('scoreDetails', {})),
                'batting_stats': self._process_batting_stats(innings_data.get('batTeamDetails', {}).get('batsmenData', {})),
                'bowling_stats': self._process_bowling_stats(innings_data.get('bowlTeamDetails', {}).get('bowlersData', {})),
                'extras': self._process_extras(innings_data.get('extrasData', {})),
                'partnerships': self._process_partnerships(innings_data.get('partnershipsData', [])),
                'wickets': self._process_wickets(innings_data.get('wicketsData', [])),
                'powerplays': self._process_powerplays(innings_data.get('ppData', {}))
            }
            innings_list.append(innings_info)
        
        return innings_list
    
    def _process_score_details(self, score_data: Dict) -> Dict[str, Any]:
        """Process score details"""
        return {
            'runs': score_data.get('runs', 0),
            'wickets': score_data.get('wickets', 0),
            'overs': score_data.get('overs', '0.0'),
            'run_rate': score_data.get('runRate', 0.0),
            'required_run_rate': score_data.get('reqRunRate', 0.0) if score_data.get('reqRunRate') else None,
            'balls_remaining': score_data.get('ballsRemaining') if score_data.get('ballsRemaining') else None,
            'runs_required': score_data.get('runsRequired') if score_data.get('runsRequired') else None
        }
    
    def _process_batting_stats(self, batting_data: Dict) -> List[Dict[str, Any]]:
        """Process batting statistics"""
        batting_stats = []
        
        for bat_key, batsman in batting_data.items():
            if isinstance(batsman, dict) and 'batId' in batsman:
                batting_stats.append({
                    'player_id': batsman.get('batId'),
                    'player_name': batsman.get('batName'),
                    'position': batsman.get('batShortName'),
                    'runs': batsman.get('runs', 0),
                    'balls_faced': batsman.get('balls', 0),
                    'fours': batsman.get('fours', 0),
                    'sixes': batsman.get('sixes', 0),
                    'strike_rate': batsman.get('strkRate', 0.0),
                    'dismissal_info': batsman.get('outDesc', 'Not Out'),
                    'is_striker': batsman.get('isStriker', False),
                    'is_non_striker': batsman.get('isNonStriker', False)
                })
        
        # Sort by batting order
        batting_stats.sort(key=lambda x: x.get('position', '11'))
        return batting_stats
    
    def _process_bowling_stats(self, bowling_data: Dict) -> List[Dict[str, Any]]:
        """Process bowling statistics"""
        bowling_stats = []
        
        for bowl_key, bowler in bowling_data.items():
            if isinstance(bowler, dict) and 'bowlId' in bowler:
                bowling_stats.append({
                    'player_id': bowler.get('bowlId'),
                    'player_name': bowler.get('bowlName'),
                    'overs': bowler.get('overs', '0.0'),
                    'maidens': bowler.get('maidens', 0),
                    'runs': bowler.get('runs', 0),
                    'wickets': bowler.get('wickets', 0),
                    'economy': bowler.get('economy', 0.0),
                    'wides': bowler.get('wides', 0),
                    'noballs': bowler.get('noballs', 0),
                    'dots': bowler.get('dots', 0) if bowler.get('dots') else None
                })
        
        return bowling_stats
    
    def _process_extras(self, extras_data: Dict) -> Dict[str, Any]:
        """Process extras information"""
        return {
            'total': extras_data.get('total', 0),
            'byes': extras_data.get('byes', 0),
            'leg_byes': extras_data.get('legByes', 0),
            'wides': extras_data.get('wides', 0),
            'noballs': extras_data.get('noBalls', 0),
            'penalty': extras_data.get('penalty', 0)
        }
    
    def _process_partnerships(self, partnerships_data: List) -> List[Dict[str, Any]]:
        """Process partnership information"""
        partnerships = []
        
        for partnership in partnerships_data:
            partnerships.append({
                'partnership_id': partnership.get('partnershipId'),
                'player1_name': partnership.get('bat1Name'),
                'player1_id': partnership.get('bat1Id'),
                'player1_runs': partnership.get('bat1Runs', 0),
                'player1_balls': partnership.get('bat1Balls', 0),
                'player2_name': partnership.get('bat2Name'),
                'player2_id': partnership.get('bat2Id'),
                'player2_runs': partnership.get('bat2Runs', 0),
                'player2_balls': partnership.get('bat2Balls', 0),
                'total_runs': partnership.get('totalRuns', 0),
                'total_balls': partnership.get('totalBalls', 0),
                'run_rate': partnership.get('runRate', 0.0)
            })
        
        return partnerships
    
    def _process_wickets(self, wickets_data: List) -> List[Dict[str, Any]]:
        """Process wickets information"""
        wickets = []
        
        for wicket in wickets_data:
            wickets.append({
                'wicket_number': wicket.get('wktNbr'),
                'batsman_name': wicket.get('batName'),
                'batsman_id': wicket.get('batId'),
                'runs': wicket.get('wktRuns'),
                'balls': wicket.get('wktBalls'),
                'dismissal_type': wicket.get('wktDesc'),
                'over': wicket.get('wktOver')
            })
        
        return wickets
    
    def _process_powerplays(self, powerplay_data: Dict) -> List[Dict[str, Any]]:
        """Process powerplay information"""
        powerplays = []
        
        if powerplay_data:
            for pp_key, pp_info in powerplay_data.items():
                if isinstance(pp_info, dict):
                    powerplays.append({
                        'type': pp_info.get('ppType'),
                        'overs_info': pp_info.get('ppOversInfo'),
                        'runs': pp_info.get('ppRuns', 0),
                        'wickets': pp_info.get('ppWickets', 0)
                    })
        
        return powerplays
    
    def _extract_live_score(self, data: Dict) -> Optional[Dict[str, Any]]:
        """Extract current live score information"""
        # This would extract live batting/bowling information
        # Implementation depends on the API structure for live data
        return None
    
    def _extract_match_status(self, data: Dict) -> Dict[str, Any]:
        """Extract match status and state"""
        match_header = data.get('matchHeader', {})
        
        return {
            'state': match_header.get('state'),
            'status': match_header.get('status'),
            'play_status': match_header.get('playStatus'),
            'result': match_header.get('result')
        }
    
    def _extract_venue(self, data: Dict) -> Dict[str, Any]:
        """Extract venue information"""
        venue_info = data.get('venueInfo', {})
        
        return {
            'id': venue_info.get('id'),
            'name': venue_info.get('ground'),
            'city': venue_info.get('city'),
            'country': venue_info.get('country'),
            'timezone': venue_info.get('timezone')
        }
    
    def _extract_officials(self, data: Dict) -> List[Dict[str, Any]]:
        """Extract match officials information"""
        # Implementation depends on API structure
        return []
    
    def _extract_weather(self, data: Dict) -> Dict[str, Any]:
        """Extract weather information"""
        # Implementation depends on API structure
        return {}
    
    def _extract_toss(self, data: Dict) -> Dict[str, Any]:
        """Extract toss information"""
        match_header = data.get('matchHeader', {})
        toss_results = match_header.get('tossResults', {})
        
        return {
            'toss_winner_id': toss_results.get('tossWinnerId'),
            'toss_winner_name': toss_results.get('tossWinnerName'),
            'decision': toss_results.get('decision')
        }
    
    def _extract_series_info(self, data: Dict) -> Dict[str, Any]:
        """Extract series information"""
        series_info = data.get('seriesInfo', {})
        
        return {
            'series_id': series_info.get('id'),
            'series_name': series_info.get('name'),
            'series_full_name': series_info.get('seriesFullName')
        }
    
    def _get_empty_scorecard(self) -> Dict[str, Any]:
        """Return empty scorecard structure"""
        return {
            'match_id': None,
            'match_info': {},
            'teams': {},
            'innings': [],
            'live_score': None,
            'match_status': {},
            'venue': {},
            'officials': [],
            'weather': {},
            'toss': {},
            'series_info': {},
            'error': 'Unable to load scorecard data'
        }

    def get_live_commentary(self, match_id: str, user=None) -> List[Dict[str, Any]]:
        """Get live commentary for a match"""
        try:
            commentary_data = self.api_manager.make_request(
                f'/mcenter/v1/{match_id}/comm', 
                user=user
            )
            
            if not commentary_data:
                return []
            
            return self._process_commentary_data(commentary_data)
            
        except Exception as e:
            logger.error(f"Error getting live commentary for match {match_id}: {str(e)}")
            return []
    
    def _process_commentary_data(self, commentary_data: Dict) -> List[Dict[str, Any]]:
        """Process commentary data"""
        comments = []
        comment_items = commentary_data.get('commentaryList', [])
        
        for item in comment_items:
            comment_info = item.get('commText', '')
            over_number = item.get('overNumber')
            ball_number = item.get('ballNbr')
            timestamp = item.get('timestamp')
            
            comments.append({
                'commentary': comment_info,
                'over': over_number,
                'ball': ball_number,
                'timestamp': timestamp,
                'innings_id': item.get('inningsId')
            })
        
        return comments