"""
WebSocket connection manager for real-time messaging
"""

from typing import Dict, List, Set
from fastapi import WebSocket
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """Manage WebSocket connections for live chat"""
    
    def __init__(self):
        # Store active connections: {question_id: {user_id: websocket, ...}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
        # Store connected user IDs for quick lookup
        self.user_connections: Dict[int, Set[int]] = {}
    
    async def connect(self, websocket: WebSocket, question_id: int, user_id: int):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        
        if question_id not in self.active_connections:
            self.active_connections[question_id] = {}
        
        self.active_connections[question_id][user_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(question_id)
        
        print(f"User {user_id} connected to question {question_id}")
    
    def disconnect(self, question_id: int, user_id: int):
        """Remove a disconnected user"""
        if question_id in self.active_connections:
            self.active_connections[question_id].pop(user_id, None)
            
            if not self.active_connections[question_id]:
                del self.active_connections[question_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id].discard(question_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        print(f"User {user_id} disconnected from question {question_id}")
    
    async def broadcast_to_question(self, question_id: int, message: dict):
        """Send message to all users in a question thread"""
        if question_id not in self.active_connections:
            return
        
        message["timestamp"] = datetime.utcnow().isoformat()
        disconnected_users = []
        
        for user_id, websocket in self.active_connections[question_id].items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(question_id, user_id)
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send message to all connected sessions of a user"""
        if user_id not in self.user_connections:
            return
        
        message["timestamp"] = datetime.utcnow().isoformat()
        disconnected_questions = []
        
        for question_id in list(self.user_connections[user_id]):
            if question_id in self.active_connections and user_id in self.active_connections[question_id]:
                try:
                    await self.active_connections[question_id][user_id].send_json(message)
                except Exception as e:
                    print(f"Error sending to user {user_id}: {e}")
                    disconnected_questions.append(question_id)
        
        # Clean up disconnected
        for question_id in disconnected_questions:
            self.disconnect(question_id, user_id)
    
    async def send_to_astrologer(self, question_id: int, astrologer_id: int, message: dict):
        """Send message to astrologer handling specific question"""
        # This would connect to the astrologer's dashboard
        if question_id in self.active_connections and astrologer_id in self.active_connections[question_id]:
            try:
                await self.active_connections[question_id][astrologer_id].send_json(message)
            except Exception as e:
                print(f"Error sending to astrologer {astrologer_id}: {e}")
    
    def get_active_users_in_question(self, question_id: int) -> List[int]:
        """Get list of active user IDs in a question"""
        if question_id not in self.active_connections:
            return []
        return list(self.active_connections[question_id].keys())
    
    def get_user_active_questions(self, user_id: int) -> List[int]:
        """Get list of question IDs user is connected to"""
        if user_id not in self.user_connections:
            return []
        return list(self.user_connections[user_id])
    
    def is_user_connected(self, user_id: int, question_id: int) -> bool:
        """Check if user is connected to specific question"""
        return (question_id in self.active_connections and 
                user_id in self.active_connections[question_id])
    
    def get_connection_count(self) -> dict:
        """Get connection statistics"""
        total_connections = sum(len(users) for users in self.active_connections.values())
        return {
            "total_connections": total_connections,
            "active_questions": len(self.active_connections),
            "active_users": len(self.user_connections)
        }


# Global connection manager instance
manager = ConnectionManager()
