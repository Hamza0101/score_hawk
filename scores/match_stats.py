def get_match_leanback(match_id, user=None, ip_address=None):
    from .api_manager import CricketAPIManager
    
    api_manager = CricketAPIManager()
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/leanback"
    
    data = api_manager.make_request(url, user=user, ip_address=ip_address)
    
    if not data:
        return None
        
        # Extract miniscore information
        miniscore = data.get('miniscore', {})
        match_header = data.get('matchHeader', {})
        
        # Format current batting information
        current_batting = {
            'striker': miniscore.get('batsmanStriker', {}),
            'non_striker': miniscore.get('batsmanNonStriker', {}),
            'team_score': miniscore.get('batTeam', {}),
            'current_partnership': miniscore.get('partnerShip', {}),
            'last_wicket': miniscore.get('lastWicket', '')
        }
        
        # Format current bowling information
        current_bowling = {
            'striker': miniscore.get('bowlerStriker', {}),
            'non_striker': miniscore.get('bowlerNonStriker', {})
        }
        
        # Match progress information
        match_progress = {
            'overs': miniscore.get('overs'),
            'current_run_rate': miniscore.get('currentRunRate'),
            'required_run_rate': miniscore.get('requiredRunRate'),
            'target': miniscore.get('target'),
            'recent_overs': miniscore.get('recentOvsStats'),
            'power_play': miniscore.get('ppData', {})
        }
        
        # Match summary
        match_summary = {
            'description': match_header.get('matchDescription'),
            'format': match_header.get('matchFormat'),
            'type': match_header.get('matchType'),
            'state': match_header.get('state'),
            'status': match_header.get('status'),
            'series': match_header.get('seriesDesc'),
            'result': match_header.get('result', {}),
            'players_of_match': match_header.get('playersOfTheMatch', []),
            'players_of_series': match_header.get('playersOfTheSeries', [])
        }
        
        # Innings details
        innings_details = miniscore.get('matchScoreDetails', {}).get('inningsScoreList', [])
        
        return {
            'current_batting': current_batting,
            'current_bowling': current_bowling,
            'match_progress': match_progress,
            'match_summary': match_summary,
            'innings_details': innings_details
        }