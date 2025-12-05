"""
Session Management Module
Handles persistent session storage and auto-login functionality
"""

import json
import os
from datetime import datetime, timedelta


class SessionManager:
    """Manages user sessions and persistent login"""
    
    def __init__(self, session_file="session.json"):
        self.session_file = session_file
        self.session_data = {}
        self.load_session()
    
    def load_session(self):
        """Load session from file"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
            except:
                self.session_data = {}
        else:
            self.session_data = {}
    
    def save_session(self):
        """Save session to file"""
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f, indent=4, default=str)
    
    def create_session(self, username):
        """Create a new session for user"""
        self.session_data = {
            "username": username,
            "login_time": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "active": True
        }
        self.save_session()
    
    def is_session_valid(self):
        """Check if session is still valid"""
        if not self.session_data or not self.session_data.get("active"):
            return False
        
        # Check if session is less than 30 days old
        try:
            login_time = datetime.fromisoformat(self.session_data["login_time"])
            if datetime.now() - login_time > timedelta(days=30):
                self.clear_session()
                return False
            return True
        except:
            return False
    
    def get_session_username(self):
        """Get username from current session"""
        if self.is_session_valid():
            return self.session_data.get("username")
        return None
    
    def update_activity(self):
        """Update last activity time"""
        if self.session_data:
            self.session_data["last_activity"] = datetime.now().isoformat()
            self.save_session()
    
    def clear_session(self):
        """Clear session"""
        self.session_data = {}
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
    
    def logout(self):
        """Logout user"""
        self.session_data["active"] = False
        self.save_session()
