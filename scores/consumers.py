import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .scorecard_manager import ScorecardManager
import logging

logger = logging.getLogger(__name__)

class LiveScoreConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for live cricket score updates"""
    
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'match_{self.match_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Start sending periodic updates for this match
        asyncio.create_task(self.send_periodic_updates())
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'ping')
            
            if message_type == 'request_update':
                await self.send_scorecard_update()
            elif message_type == 'request_commentary':
                await self.send_commentary_update()
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': asyncio.get_event_loop().time()
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
    
    async def send_periodic_updates(self):
        """Send periodic score updates every 30 seconds"""
        while True:
            try:
                await asyncio.sleep(30)  # Update every 30 seconds
                await self.send_scorecard_update()
            except Exception as e:
                logger.error(f"Error in periodic updates: {str(e)}")
                break
    
    async def send_scorecard_update(self):
        """Send scorecard update to client"""
        try:
            user = self.scope["user"] if self.scope["user"].is_authenticated else None
            scorecard_data = await self.get_scorecard_data(self.match_id, user)
            
            await self.send(text_data=json.dumps({
                'type': 'scorecard_update',
                'match_id': self.match_id,
                'data': scorecard_data,
                'timestamp': asyncio.get_event_loop().time()
            }))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to get scorecard update: {str(e)}'
            }))
    
    async def send_commentary_update(self):
        """Send commentary update to client"""
        try:
            user = self.scope["user"] if self.scope["user"].is_authenticated else None
            commentary_data = await self.get_commentary_data(self.match_id, user)
            
            await self.send(text_data=json.dumps({
                'type': 'commentary_update',
                'match_id': self.match_id,
                'commentary': commentary_data,
                'timestamp': asyncio.get_event_loop().time()
            }))
            
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Failed to get commentary update: {str(e)}'
            }))
    
    # Group message handlers
    async def score_update(self, event):
        """Handle score update messages sent to the group"""
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'data': event['data']
        }))
    
    async def match_event(self, event):
        """Handle match event messages (wicket, boundary, etc.)"""
        await self.send(text_data=json.dumps({
            'type': 'match_event',
            'event_type': event['event_type'],
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_scorecard_data(self, match_id, user):
        """Get scorecard data asynchronously"""
        scorecard_manager = ScorecardManager()
        return scorecard_manager.get_enhanced_scorecard(match_id, user=user)
    
    @database_sync_to_async
    def get_commentary_data(self, match_id, user):
        """Get commentary data asynchronously"""
        scorecard_manager = ScorecardManager()
        return scorecard_manager.get_live_commentary(match_id, user=user)


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for general notifications"""
    
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_authenticated:
            self.user_group_name = f'user_{self.user.id}'
            
            # Join user group
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'ping')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': asyncio.get_event_loop().time()
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
    
    # Group message handlers
    async def user_notification(self, event):
        """Handle user notification messages"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['data']
        }))