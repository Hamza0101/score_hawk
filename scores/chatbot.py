import google.generativeai as genai
import os
import json
from django.conf import settings
from django.contrib.auth.models import User
from typing import Dict, List, Any, Optional
from .api_manager import CricketAPIManager
from .scorecard_manager import ScorecardManager
import logging

logger = logging.getLogger(__name__)

class CricketChatbot:
    """AI-powered cricket chatbot using Google Gemini"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        logger.info(f"Initializing CricketChatbot with API key: {'***' if self.api_key else 'None'}")
        
        if self.api_key and self.api_key != 'your-gemini-api-key-here':
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Successfully configured Gemini model")
            except Exception as e:
                logger.error(f"Failed to configure Gemini: {e}")
                self.model = None
        else:
            logger.info("No valid Gemini API key found, using fallback responses")
            self.model = None
        
        self.api_manager = CricketAPIManager()
        self.scorecard_manager = ScorecardManager()
        
        # Cricket knowledge base for when APIs are unavailable
        self.cricket_knowledge = {
            'players': {
                'virat kohli': {
                    'full_name': 'Virat Kohli',
                    'country': 'India',
                    'role': 'Batsman',
                    'born': '5 November 1988, Delhi, India',
                    'international_debut': 'ODI: 18 August 2008 vs Sri Lanka, Test: 20 June 2011 vs West Indies',
                    'career_highlights': [
                        'Former Indian cricket team captain (2017-2022)',
                        'One of the greatest batsmen of all time',
                        'Over 26,000 international runs across all formats',
                        '75+ international centuries',
                        'ICC Cricketer of the Year 2017 and 2018',
                        'Wisden Leading Cricketer in the World 2016, 2017, 2018'
                    ],
                    'records': [
                        'Most runs in T20I cricket',
                        'Fastest player to 8,000, 9,000, 10,000, 11,000, and 12,000 ODI runs',
                        'Most centuries in successful ODI chases',
                        'Most runs in IPL history'
                    ],
                    'current_teams': 'Royal Challengers Bangalore (IPL), India'
                },
                'babar azam': {
                    'full_name': 'Babar Azam',
                    'country': 'Pakistan',
                    'role': 'Batsman',
                    'born': '15 October 1994, Lahore, Pakistan',
                    'international_debut': 'ODI: 31 May 2015 vs Zimbabwe, Test: 13 October 2016 vs West Indies',
                    'career_highlights': [
                        'Current Pakistan cricket team captain',
                        'No.1 ranked ODI and T20I batsman (former)',
                        'Youngest player to score 3,000 T20I runs',
                        'First Pakistani to score centuries in first 4 Test matches as captain'
                    ],
                    'current_teams': 'Peshawar Zalmi (PSL), Pakistan'
                },
                'steve smith': {
                    'full_name': 'Steven Peter Devereux Smith',
                    'country': 'Australia',
                    'role': 'Batsman',
                    'born': '2 June 1989, Sydney, Australia',
                    'international_debut': 'T20I: 17 February 2010 vs Pakistan, Test: 13 July 2010 vs Pakistan',
                    'career_highlights': [
                        'Former Australian cricket team captain',
                        'One of the best Test batsmen in modern cricket',
                        'ICC Test Player of the Decade (2011-2020)',
                        '30+ Test centuries'
                    ],
                    'current_teams': 'Sydney Sixers (BBL), Australia'
                }
            },
            'teams': {
                'india': {
                    'full_name': 'India National Cricket Team',
                    'captain': 'Rohit Sharma',
                    'coach': 'Rahul Dravid',
                    'major_achievements': [
                        'ICC Cricket World Cup: 1983, 2011',
                        'ICC T20 World Cup: 2007, 2024',
                        'ICC Champions Trophy: 2002, 2013',
                        'World Test Championship: 2021'
                    ]
                },
                'australia': {
                    'full_name': 'Australia National Cricket Team',
                    'captain': 'Pat Cummins',
                    'coach': 'Andrew McDonald',
                    'major_achievements': [
                        'ICC Cricket World Cup: 1987, 1999, 2003, 2007, 2015, 2023',
                        'ICC T20 World Cup: 2021',
                        'World Test Championship: 2023'
                    ]
                }
            }
        }
        
        # System prompt for cricket context
        self.system_prompt = """
        You are CricBot, an expert cricket assistant for Score Hawk - a comprehensive cricket information platform.
        
        You are an expert on ALL aspects of cricket including:
        - Player profiles, careers, statistics, and achievements
        - Team information, history, and current form
        - Cricket rules, formats, and terminology
        - Historical records and memorable matches
        - Current tournaments and series
        - Cricket strategies and techniques
        
        REAL-TIME DATA: When "Current cricket data" is provided in the context, use it to enhance your responses with the latest information about matches, rankings, and news.
        
        COMPREHENSIVE KNOWLEDGE: Even without real-time data, you should provide detailed, accurate information about:
        - Famous cricketers (their careers, achievements, playing style, records)
        - Cricket history and iconic moments
        - Rules and regulations
        - Team dynamics and rivalries
        - Cricket formats (Test, ODI, T20, domestic leagues)
        
        RESPONSE STYLE:
        - Be knowledgeable and detailed when discussing cricket topics
        - Provide context and background information
        - Use specific examples and statistics when relevant
        - Be conversational but informative
        - If you have real-time data, incorporate it naturally
        - For player questions, include career highlights, achievements, and current status
        
        Answer cricket questions comprehensively using your full knowledge base.
        """
    
    def get_response(self, message: str, user: Optional[User] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Get AI response for user message"""
        
        logger.info(f"Getting response for message: {message[:50]}...")
        
        if not self.model:
            logger.info("No Gemini model available, using fallback responses")
            return self._get_fallback_response(message, user, context)
        
        try:
            logger.info("Using Gemini model for response")
            
            # Prepare conversation context
            conversation_context = self._prepare_context(message, user, context)
            
            # Create the full prompt with system context
            full_prompt = f"{self.system_prompt}\n\nUser: {conversation_context}\n\nCricBot:"
            
            # Make Gemini request
            logger.info("Making request to Gemini API")
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                )
            )
            
            ai_response = response.text.strip() if response.text else "I apologize, but I couldn't generate a response. Please try again."
            logger.info(f"Received Gemini response: {ai_response[:100]}...")
            
            # Check if we need to fetch real-time data
            enhanced_response = self._enhance_with_cricket_data(ai_response, message, user)
            
            return {
                'response': enhanced_response,
                'success': True,
                'tokens_used': len(full_prompt) + len(ai_response),  # Approximate token count
                'source': 'gemini'
            }
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                logger.warning(f"Gemini API rate limit exceeded: {error_msg}")
            else:
                logger.error(f"Error in Gemini chatbot response: {error_msg}")
            
            logger.info("Falling back to predefined responses")
            fallback_response = self._get_fallback_response(message, user, context)
            fallback_response['source'] = 'fallback'
            fallback_response['reason'] = 'rate_limit' if "429" in error_msg else 'error'
            return fallback_response
    
    def _prepare_context(self, message: str, user: Optional[User], context: Optional[Dict]) -> str:
        """Prepare conversation context with user data and real-time cricket information"""
        context_parts = [message]
        
        if user and user.is_authenticated:
            context_parts.append(f"User: {user.get_full_name() or user.username}")
        
        if context:
            if 'current_match' in context:
                context_parts.append(f"Currently viewing match: {context['current_match']}")
            if 'current_player' in context:
                context_parts.append(f"Currently viewing player: {context['current_player']}")
            if 'page_type' in context:
                context_parts.append(f"Current page: {context['page_type']}")
        
        # ALWAYS fetch comprehensive cricket data for any cricket question
        cricket_data = self._fetch_relevant_cricket_data(message)
        external_context = self._get_external_cricket_context(message)
        
        # Combine all cricket information
        all_cricket_info = []
        if cricket_data:
            all_cricket_info.append(cricket_data)
        if external_context:
            all_cricket_info.append(external_context)
        
        if all_cricket_info:
            context_parts.append(f"Cricket Information: {' | '.join(all_cricket_info)}")
            logger.info(f"Added comprehensive cricket data to context for: {message[:50]}")
        
        return " | ".join(context_parts)
    
    def _fetch_relevant_cricket_data(self, message: str) -> str:
        """Proactively fetch comprehensive real-time cricket data for any cricket question"""
        cricket_info = []
        message_lower = message.lower()
        
        try:
            logger.info(f"Proactively fetching real-time cricket data for: {message[:50]}")
            
            # ALWAYS fetch core cricket data for context
            data_fetched = []
            
            # 1. LIVE/RECENT MATCHES - Always fetch for current cricket context
            try:
                recent_matches = self.api_manager.make_request('/matches/v1/recent', cache_enabled=True)
                if recent_matches and isinstance(recent_matches, dict):
                    type_matches = recent_matches.get('typeMatches', [])
                    all_matches = []
                    live_matches = []
                    
                    for match_type in type_matches:
                        for series in match_type.get('seriesMatches', []):
                            for match in series.get('seriesAdWrapper', {}).get('matches', []):
                                match_info = match.get('matchInfo', {})
                                status = match_info.get('status', 'Complete')
                                state = match_info.get('state', 'Complete')
                                
                                match_data = {
                                    'team1': match_info.get('team1', {}).get('teamSName', 'Team1'),
                                    'team2': match_info.get('team2', {}).get('teamSName', 'Team2'),
                                    'status': status,
                                    'venue': match_info.get('venueInfo', {}).get('ground', 'Unknown'),
                                    'series': series.get('seriesAdWrapper', {}).get('seriesName', 'Unknown Series')
                                }
                                
                                if state.lower() in ['live', 'in progress'] or 'live' in status.lower():
                                    live_matches.append(match_data)
                                else:
                                    all_matches.append(match_data)
                    
                    if live_matches:
                        cricket_info.append("🔴 LIVE MATCHES: " + "; ".join([
                            f"{m['team1']} vs {m['team2']} ({m['status']}) at {m['venue']}" 
                            for m in live_matches[:3]
                        ]))
                        data_fetched.append("live matches")
                    elif all_matches:
                        cricket_info.append("📊 RECENT MATCHES: " + "; ".join([
                            f"{m['team1']} vs {m['team2']} ({m['status']}) at {m['venue']}" 
                            for m in all_matches[:5]
                        ]))
                        data_fetched.append("recent matches")
            except Exception as e:
                logger.warning(f"Failed to fetch match data: {e}")
            
            # 2. CURRENT PLAYER RANKINGS - Always fetch for player context
            try:
                # Get batting rankings
                batsmen_rankings = self.api_manager.make_request('/stats/v1/rankings/batsmen', cache_enabled=True)
                if batsmen_rankings and isinstance(batsmen_rankings, dict):
                    top_batsmen = batsmen_rankings.get('rank', [])[:15]  # More players for better context
                    if top_batsmen:
                        cricket_info.append("🏏 TOP BATSMEN RANKINGS: " + "; ".join([
                            f"{i+1}. {player.get('name', 'Unknown')} ({player.get('rating', 'N/A')} pts)"
                            for i, player in enumerate(top_batsmen)
                        ]))
                        data_fetched.append("batting rankings")
                
                # Get bowling rankings
                bowler_rankings = self.api_manager.make_request('/stats/v1/rankings/bowlers', cache_enabled=True)
                if bowler_rankings and isinstance(bowler_rankings, dict):
                    top_bowlers = bowler_rankings.get('rank', [])[:15]
                    if top_bowlers:
                        cricket_info.append("🎳 TOP BOWLER RANKINGS: " + "; ".join([
                            f"{i+1}. {player.get('name', 'Unknown')} ({player.get('rating', 'N/A')} pts)"
                            for i, player in enumerate(top_bowlers)
                        ]))
                        data_fetched.append("bowling rankings")
            except Exception as e:
                logger.warning(f"Failed to fetch player rankings: {e}")
            
            # 3. TEAM RANKINGS - Always fetch for team context
            try:
                for format_type in ['test', 'odi', 't20']:
                    team_rankings = self.api_manager.make_request('/stats/v1/rankings/teams', 
                                                                params={'formatType': format_type}, 
                                                                cache_enabled=True)
                    if team_rankings and isinstance(team_rankings, dict):
                        top_teams = team_rankings.get('rank', [])[:8]
                        if top_teams:
                            format_name = format_type.upper()
                            cricket_info.append(f"🏆 {format_name} TEAM RANKINGS: " + "; ".join([
                                f"{i+1}. {team.get('name', 'Unknown')} ({team.get('rating', 'N/A')} pts)"
                                for i, team in enumerate(top_teams)
                            ]))
                            data_fetched.append(f"{format_type} team rankings")
                            break  # Get at least one format
            except Exception as e:
                logger.warning(f"Failed to fetch team rankings: {e}")
            
            # 4. LATEST CRICKET NEWS - Always fetch for current context
            try:
                news_data = self.api_manager.make_request('/news/v1/index', cache_enabled=True)
                if news_data and isinstance(news_data, dict):
                    stories = news_data.get('storyList', [])[:5]
                    recent_news = []
                    for story in stories:
                        if 'story' in story:
                            story_info = story['story']
                            headline = story_info.get('hline', 'Cricket News')
                            if headline and len(headline) > 10:  # Filter out empty/short headlines
                                recent_news.append(headline)
                    
                    if recent_news:
                        cricket_info.append("📰 LATEST CRICKET NEWS: " + "; ".join(recent_news))
                        data_fetched.append("latest news")
            except Exception as e:
                logger.warning(f"Failed to fetch news data: {e}")
            
            # 5. ADDITIONAL CONTEXT-SPECIFIC DATA
            # If question mentions specific players, try to get more specific data
            famous_players = ['kohli', 'dhoni', 'babar', 'smith', 'root', 'williamson', 'warner', 'rohit', 'bumrah', 'anderson']
            if any(player in message_lower for player in famous_players):
                # Could add player-specific stats API calls here
                logger.info("Player-specific query detected - using comprehensive rankings data")
            
            # If question mentions specific teams, could fetch team-specific data
            teams = ['india', 'australia', 'england', 'pakistan', 'south africa', 'new zealand', 'sri lanka', 'bangladesh']
            if any(team in message_lower for team in teams):
                logger.info("Team-specific query detected - using comprehensive team data")
            
            if cricket_info:
                logger.info(f"Successfully fetched real-time data: {', '.join(data_fetched)}")
            else:
                logger.warning("No real-time cricket data could be fetched")
                
        except Exception as e:
            logger.error(f"Error in proactive cricket data fetching: {e}")
        
        return " | ".join(cricket_info) if cricket_info else ""
    
    def _get_external_cricket_context(self, message: str) -> str:
        """Fetch additional cricket context from external sources if needed"""
        external_info = []
        
        try:
            # Add comprehensive cricket knowledge base that's always available
            message_lower = message.lower()
            
            # Famous players knowledge base
            if any(name in message_lower for name in ['kohli', 'virat']):
                external_info.append("PLAYER CONTEXT: Virat Kohli - Indian batting legend, former captain, 75+ international centuries, Royal Challengers Bangalore (IPL), known for aggressive batting and chase specialist")
            
            elif any(name in message_lower for name in ['dhoni', 'ms dhoni']):
                external_info.append("PLAYER CONTEXT: MS Dhoni - Former Indian captain and wicket-keeper, 2011 World Cup winner, helicopter shot specialist, Chennai Super Kings captain, finished career as one of greatest finishers")
            
            elif any(name in message_lower for name in ['babar', 'azam']):
                external_info.append("PLAYER CONTEXT: Babar Azam - Current Pakistan captain, top-order batsman, former #1 ODI and T20I ranked batsman, Peshawar Zalmi (PSL)")
            
            elif any(name in message_lower for name in ['smith', 'steve smith']):
                external_info.append("PLAYER CONTEXT: Steve Smith - Australian batsman, former captain, ICC Test Player of the Decade 2011-2020, unique batting technique, Sydney Sixers (BBL)")
            
            # Team contexts
            if 'india' in message_lower and 'team' in message_lower:
                external_info.append("TEAM CONTEXT: India - Current captain: Rohit Sharma, Coach: Rahul Dravid, Recent achievements: T20 World Cup 2024, World Test Championship 2021")
            
            elif 'australia' in message_lower and 'team' in message_lower:
                external_info.append("TEAM CONTEXT: Australia - Current captain: Pat Cummins, Recent achievements: ODI World Cup 2023, World Test Championship 2023")
            
            # Cricket formats and rules
            if any(term in message_lower for term in ['lbw', 'leg before wicket']):
                external_info.append("RULE CONTEXT: LBW (Leg Before Wicket) - Ball must pitch in line, impact in line, and be hitting stumps. Umpire's call if marginal. Technology (DRS) helps review decisions")
            
            elif any(term in message_lower for term in ['drs', 'decision review']):
                external_info.append("TECHNOLOGY CONTEXT: DRS (Decision Review System) - Uses ball-tracking, edge detection, and impact prediction. Each team gets limited reviews per innings")
            
            # Tournament contexts
            if any(term in message_lower for term in ['world cup', 'wc']):
                external_info.append("TOURNAMENT CONTEXT: ICC Cricket World Cup - Premier ODI tournament, held every 4 years. Recent winners: Australia (2023), England (2019), Australia (2015)")
            
            elif any(term in message_lower for term in ['ipl', 'indian premier league']):
                external_info.append("LEAGUE CONTEXT: IPL (Indian Premier League) - World's most popular T20 league, features international stars, auction system, plays March-May annually")
            
        except Exception as e:
            logger.warning(f"Error fetching external cricket context: {e}")
        
        return " | ".join(external_info) if external_info else ""
    
    def _get_fallback_response(self, message: str, user: Optional[User], context: Optional[Dict]) -> Dict[str, Any]:
        """Provide fallback responses with real-time cricket data"""
        message_lower = message.lower()
        
        # Get real-time cricket data for enhanced fallback responses
        cricket_data = self._fetch_relevant_cricket_data(message)
        
        # Cricket-specific responses with real data
        if any(keyword in message_lower for keyword in ['hello', 'hi', 'hey']):
            response = "Hello! I'm CricBot, your cricket assistant powered by Google Gemini. I can provide real-time cricket information, live scores, and player stats."
            if cricket_data:
                response += f"\n\n📊 **Current Cricket Updates:**\n{cricket_data.replace(' | ', '\n• ')}"
        
        elif any(keyword in message_lower for keyword in ['live score', 'current score', 'latest score', 'live match']):
            response = "🏏 **Live Cricket Updates:**"
            if cricket_data and 'LIVE MATCHES' in cricket_data:
                live_info = [part for part in cricket_data.split(' | ') if 'LIVE MATCHES' in part][0]
                response += f"\n{live_info.replace('LIVE MATCHES: ', '').replace(';', '\n•')}"
            else:
                response += "\nNo live matches currently. Check recent matches for latest scores."
            
        elif any(keyword in message_lower for keyword in ['team ranking', 'rankings', 'position']):
            response = "📊 **Team Rankings:**"
            if cricket_data and 'TEAM RANKINGS' in cricket_data:
                rankings_info = [part for part in cricket_data.split(' | ') if 'TEAM RANKINGS' in part][0]
                response += f"\n{rankings_info.replace('TEAM RANKINGS: ', '').replace(';', '\n')}"
            else:
                response += "\nVisit the Rankings section for the latest ICC rankings for Test, ODI, and T20 cricket."
            
        elif any(keyword in message_lower for keyword in ['batsman', 'batting', 'runs']):
            response = "🏏 **Top Batsmen Rankings:**"
            if cricket_data and 'TOP BATSMEN' in cricket_data:
                batsmen_info = [part for part in cricket_data.split(' | ') if 'TOP BATSMEN' in part][0]
                response += f"\n{batsmen_info.replace('TOP BATSMEN: ', '').replace(';', '\n')}"
            else:
                response += "\nUse the Players section to search for detailed batting statistics and rankings."
                
        elif any(keyword in message_lower for keyword in ['bowler', 'bowling', 'wickets']):
            response = "🎳 **Top Bowlers Rankings:**"
            if cricket_data and 'TOP BOWLERS' in cricket_data:
                bowlers_info = [part for part in cricket_data.split(' | ') if 'TOP BOWLERS' in part][0]
                response += f"\n{bowlers_info.replace('TOP BOWLERS: ', '').replace(';', '\n')}"
            else:
                response += "\nUse the Players section to search for detailed bowling statistics and rankings."
            
        elif any(keyword in message_lower for keyword in ['news', 'latest news', 'update']):
            response = "📰 **Latest Cricket News:**"
            if cricket_data and 'LATEST NEWS' in cricket_data:
                news_info = [part for part in cricket_data.split(' | ') if 'LATEST NEWS' in part][0]
                response += f"\n{news_info.replace('LATEST NEWS: ', '').replace(';', '\n• ')}"
            else:
                response += "\nCheck out the News section for breaking cricket news, match reports, and player updates."
            
        elif any(keyword in message_lower for keyword in ['rule', 'rules', 'law', 'lbw']):
            response = "📚 Cricket rules can be complex! Here are some key points:\n\n• LBW: Ball hits pad in line with stumps, would have hit stumps\n• Powerplay: Fielding restrictions in limited overs cricket\n• Free hit: After a no-ball, next ball can't be out (except run-out)\n• DRS: Teams can review umpire decisions\n\nWhat specific rule would you like to know about?"
            
        elif any(keyword in message_lower for keyword in ['match format', 'test', 'odi', 't20']):
            response = "🏏 Cricket Formats:\n\n• **Test Cricket**: 5 days, 2 innings per team, unlimited overs\n• **ODI**: 50 overs per side, colored clothing, day/night matches\n• **T20**: 20 overs per side, shortest format, high entertainment\n\nEach format has its own excitement and strategy!"
            
        elif any(keyword in message_lower for keyword in ['thank', 'thanks']):
            response = "You're welcome! Happy to help with your cricket queries. Feel free to ask anything about cricket - scores, players, rules, or stats!"
            
        else:
            response = "🏏 I'm here to help with cricket!"
            if cricket_data:
                response += f"\n\n📊 **Current Cricket Information:**\n{cricket_data.replace(' | ', '\n• ')}"
            response += "\n\nI can assist you with:\n• Live scores and match updates\n• Player statistics and information\n• Team rankings and records\n• Cricket rules and formats\n• Latest cricket news\n\nWhat would you like to know about cricket today?"
        
        return {
            'response': response,
            'success': True,
            'tokens_used': 0
        }
    
    def _enhance_with_cricket_data(self, ai_response: str, original_message: str, user: Optional[User]) -> str:
        """Enhance AI response with additional cricket data context if needed"""
        # This method is now primarily used by the main get_response method
        # Most real-time data integration is now handled in _fetch_relevant_cricket_data
        return ai_response
    
    def get_suggested_questions(self, context: Optional[Dict] = None) -> List[str]:
        """Get suggested questions based on context"""
        
        base_suggestions = [
            "What are the current live matches?",
            "Who are the top batsmen in ODI cricket?",
            "Explain the LBW rule in cricket",
            "What's the latest cricket news?",
            "Compare Virat Kohli and Steve Smith",
        ]
        
        if context:
            if context.get('page_type') == 'match':
                return [
                    "Give me the match summary",
                    "Who are the key players to watch?",
                    "What's the pitch condition like?",
                    "Predict the match outcome",
                    "Show me the team comparison"
                ]
            elif context.get('page_type') == 'player':
                return [
                    "Analyze this player's performance",
                    "Compare with other players",
                    "What are their career highlights?",
                    "Show recent form",
                    "Career statistics breakdown"
                ]
            elif context.get('page_type') == 'rankings':
                return [
                    "Explain the ranking system",
                    "Who might move up next?",
                    "Historical ranking trends",
                    "Compare team strengths",
                    "Upcoming series impact"
                ]
        
        return base_suggestions
    
    def process_quick_query(self, query_type: str, params: Dict, user: Optional[User] = None) -> Dict[str, Any]:
        """Process quick queries like scores, stats, etc."""
        
        try:
            if query_type == 'live_scores':
                matches = self.api_manager.make_request('/matches/v1/recent')
                if matches and isinstance(matches, list):
                    live_matches = [m for m in matches[:5] if m.get('status', '').lower() == 'live']
                else:
                    live_matches = []
                
                if live_matches:
                    response = "🔴 **Live Matches:**\n"
                    for match in live_matches:
                        response += f"• {match.get('description', 'Match')} - {match.get('status', '')}\n"
                    return {'response': response, 'success': True}
                else:
                    return {'response': "No live matches currently. Check recent matches for latest scores.", 'success': True}
            
            elif query_type == 'player_search':
                player_name = params.get('name', '')
                if player_name:
                    # This would integrate with player search
                    return {'response': f"Searching for player: {player_name}", 'success': True}
            
            elif query_type == 'team_rankings':
                rankings = self.api_manager.make_request('/stats/v1/rankings/teams')
                if rankings:
                    response = "🏏 **Team Rankings (Test):**\n"
                    for i, team in enumerate(rankings.get('rank', [])[:5], 1):
                        response += f"{i}. {team.get('name', '')} - {team.get('rating', '')} pts\n"
                    return {'response': response, 'success': True}
            
            return {'response': 'Query type not supported', 'success': False}
            
        except Exception as e:
            logger.error(f"Error in quick query: {e}")
            return {'response': 'Error processing query', 'error': str(e), 'success': False}


class ChatSession:
    """Manage chat session for a user"""
    
    def __init__(self, user: Optional[User] = None, session_key: Optional[str] = None):
        self.user = user
        self.session_key = session_key
        self.chatbot = CricketChatbot()
        self.conversation_history = []
    
    def add_message(self, message: str, is_user: bool = True, context: Optional[Dict] = None):
        """Add message to conversation history"""
        self.conversation_history.append({
            'message': message,
            'is_user': is_user,
            'timestamp': None,  # Would use timezone.now() in Django
            'context': context
        })
    
    def get_response(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Get chatbot response and update conversation"""
        
        # Add user message to history
        self.add_message(message, is_user=True, context=context)
        
        # Get AI response
        response_data = self.chatbot.get_response(message, self.user, context)
        
        # Add AI response to history
        if response_data.get('success'):
            self.add_message(response_data['response'], is_user=False)
        
        return response_data
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_suggested_questions(self, context: Optional[Dict] = None) -> List[str]:
        """Get suggested questions for current context"""
        return self.chatbot.get_suggested_questions(context)