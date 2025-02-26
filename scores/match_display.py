from .cricbuzz_api import get_match_details, get_match_scorecard

def process_match_data(match_id):
    """
    Process and format match data for display
    """
    match_data = get_match_details(match_id)
    if not match_data:
        return None
    
    # Process current batting information
    if 'current_batting' in match_data:
        striker = match_data['current_batting']['striker']
        non_striker = match_data['current_batting']['non_striker']
        team_score = match_data['current_batting']['team_score']
        
        # Format striker information
        striker['batName'] = striker.get('name', '')
        striker['batRuns'] = striker.get('runs', 0)
        striker['batBalls'] = striker.get('balls', 0)
        striker['batFours'] = striker.get('fours', 0)
        striker['batSixes'] = striker.get('sixes', 0)
        striker['batStrikeRate'] = striker.get('strike_rate', 0.0)
        
        # Format non-striker information
        non_striker['batName'] = non_striker.get('name', '')
        non_striker['batRuns'] = non_striker.get('runs', 0)
        non_striker['batBalls'] = non_striker.get('balls', 0)
        non_striker['batFours'] = non_striker.get('fours', 0)
        non_striker['batSixes'] = non_striker.get('sixes', 0)
        non_striker['batStrikeRate'] = non_striker.get('strike_rate', 0.0)
        
        # Format team score
        match_data['current_batting']['team_score'] = {
            'teamId': team_score.get('team_id', 0),
            'teamName': team_score.get('team_name', ''),
            'teamScore': team_score.get('runs', 0),
            'teamWkts': team_score.get('wickets', 0)
        }
    
    # Process current bowling information
    if 'current_bowling' in match_data:
        bowler = match_data['current_bowling']['striker']
        non_striker_bowler = match_data['current_bowling']['non_striker']
        
        # Format current bowler information
        bowler['bowlName'] = bowler.get('name', '')
        bowler['bowlOvers'] = bowler.get('overs', 0)
        bowler['bowlMaidens'] = bowler.get('maidens', 0)
        bowler['bowlRuns'] = bowler.get('runs', 0)
        bowler['bowlWickets'] = bowler.get('wickets', 0)
        bowler['bowlEconomy'] = bowler.get('economy', 0.0)
        bowler['bowlNoballs'] = bowler.get('noballs', 0)
        bowler['bowlWides'] = bowler.get('wides', 0)
        
        # Format non-striker bowler information
        non_striker_bowler['bowlName'] = non_striker_bowler.get('name', '')
        non_striker_bowler['bowlOvers'] = non_striker_bowler.get('overs', 0)
        non_striker_bowler['bowlMaidens'] = non_striker_bowler.get('maidens', 0)
        non_striker_bowler['bowlRuns'] = non_striker_bowler.get('runs', 0)
        non_striker_bowler['bowlWickets'] = non_striker_bowler.get('wickets', 0)
        non_striker_bowler['bowlEconomy'] = non_striker_bowler.get('economy', 0.0)
        non_striker_bowler['bowlNoballs'] = non_striker_bowler.get('noballs', 0)
        non_striker_bowler['bowlWides'] = non_striker_bowler.get('wides', 0)

    # Get detailed scorecard
    scorecard = get_match_scorecard(match_id)
    if scorecard:
        processed_scorecard = {'innings': [], 'matchHeader': scorecard.get('matchHeader', {})}
        
        for inning_key in ['0', '1']:
            if inning_key not in scorecard:
                continue
                
            inning = scorecard[inning_key]
            bat_team_details = inning.get('batTeamDetails', {})
            bowl_team_details = inning.get('bowlTeamDetails', {})
            score_details = inning.get('scoreDetails', {})
            
            processed_inning = {
                'batting_team': bat_team_details.get('batTeamName', ''),
                'total_score': score_details.get('runs', 0),
                'wickets': score_details.get('wickets', 0),
                'overs': format_overs(score_details.get('overs', '0.0')),
                'extras': inning.get('extrasData', {}).get('total', 0),
                'batting': [],
                'bowling': []
            }
            
            # Process batsmen data
            batsmen_data = bat_team_details.get('batsmenData', {})
            for bat_key, batsman in batsmen_data.items():
                if not isinstance(batsman, dict):
                    continue
                processed_batsman = {
                    'name': batsman.get('batName', ''),
                    'runs': batsman.get('runs', 0),
                    'balls': batsman.get('balls', 0),
                    'fours': batsman.get('fours', 0),
                    'sixes': batsman.get('sixes', 0),
                    'strike_rate': format_strike_rate(batsman.get('runs', 0), batsman.get('balls', 0)),
                    'dismissal': batsman.get('outDesc', 'not out')
                }
                processed_inning['batting'].append(processed_batsman)
            
            # Process bowlers data
            bowlers_data = bowl_team_details.get('bowlersData', {})
            for bowl_key, bowler in bowlers_data.items():
                if not isinstance(bowler, dict):
                    continue
                processed_bowler = {
                    'name': bowler.get('bowlName', ''),
                    'overs': format_overs(bowler.get('overs', '0.0')),
                    'maidens': bowler.get('maidens', 0),
                    'runs': bowler.get('runs', 0),
                    'wickets': bowler.get('wickets', 0),
                    'economy': format_economy(bowler.get('runs', 0), bowler.get('overs', '0.0'))
                }
                processed_inning['bowling'].append(processed_bowler)
            
            processed_scorecard['innings'].append(processed_inning)
        
        match_data['scorecard'] = processed_scorecard
    else:
        match_data['scorecard'] = None

    return match_data

def format_overs(overs):
    """
    Format overs display (e.g., 12.4)
    """
    if not overs:
        return '0.0'
    try:
        if isinstance(overs, str) and '.' in overs:
            main_overs, balls = overs.split('.')
            return f"{main_overs}.{balls}"
        return str(overs)
    except (ValueError, AttributeError):
        return '0.0'

def format_economy(runs, overs):
    """
    Calculate and format economy rate
    """
    try:
        if not overs:
            return '0.00'
        overs_parts = str(overs).split('.')
        total_balls = int(overs_parts[0]) * 6 + (int(overs_parts[1]) if len(overs_parts) > 1 else 0)
        if total_balls == 0:
            return '0.00'
        economy = (float(runs) * 6) / total_balls
        return f'{economy:.2f}'
    except (ValueError, ZeroDivisionError, IndexError):
        return '0.00'

def format_strike_rate(runs, balls):
    """
    Calculate and format strike rate
    """
    try:
        if not balls:
            return '0.00'
        strike_rate = (float(runs) * 100) / float(balls)
        return f'{strike_rate:.2f}'
    except (ValueError, ZeroDivisionError):
        return '0.00'

def format_run_rate(runs, overs):
    """
    Calculate and format run rate
    """
    try:
        if not overs:
            return '0.00'
        overs_parts = str(overs).split('.')
        total_balls = int(overs_parts[0]) * 6 + (int(overs_parts[1]) if len(overs_parts) > 1 else 0)
        if total_balls == 0:
            return '0.00'
        run_rate = (float(runs) * 6) / total_balls
        return f'{run_rate:.2f}'
    except (ValueError, ZeroDivisionError, IndexError):
        return '0.00'