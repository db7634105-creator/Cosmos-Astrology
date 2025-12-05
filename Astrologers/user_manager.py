"""
User Management Module
Handles user authentication, session management, and persistent login
"""

import json
import os
from datetime import datetime


class UserManager:
    """Manages user login, registration, and session persistence"""
    
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users_db = {}
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users_db = json.load(f)
            except:
                self.users_db = {}
        else:
            self.users_db = {}
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users_db, f, indent=4, default=str)
    
    def register_user(self, username, email, phone, password, region=None):
        """Register a new user
        
        Args:
            username: Username
            email: Email address
            phone: Phone number
            password: Password
            region: User's country/region (nepal, india, etc.)
        """
        if username in self.users_db:
            return False, "Username already exists"
        
        if not username or not email or not password:
            return False, "Please fill all required fields"
        
        self.users_db[username] = {
            "email": email,
            "phone": phone,
            "password": password,
            "region": region or "others",
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        self.save_users()
        self.current_user = username
        return True, f"User {username} registered successfully"
    
    def login_user(self, username, password):
        """Login an existing user"""
        if username not in self.users_db:
            return False, "User not found"
        
        user = self.users_db[username]
        if user['password'] != password:
            return False, "Invalid password"
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        self.save_users()
        self.current_user = username
        return True, "Login successful"
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user
    
    def logout_user(self):
        """Logout current user"""
        self.current_user = None
    
    def get_user_info(self, username=None):
        """Get user information"""
        if username is None:
            username = self.current_user
        
        if username in self.users_db:
            user = self.users_db[username]
            return {
                "username": username,
                "email": user.get("email"),
                "phone": user.get("phone"),
                "region": user.get("region", "others"),
                "created_at": user.get("created_at"),
                "last_login": user.get("last_login")
            }
        return None
    
    def get_user_region(self, username=None):
        """Get user's registered region/country"""
        if username is None:
            username = self.current_user
        
        if username in self.users_db:
            return self.users_db[username].get("region", "others")
        return "others"
    
    def update_user_region(self, username, region):
        """Update user's region/country"""
        if username not in self.users_db:
            return False, "User not found"
        
        self.users_db[username]['region'] = region
        self.save_users()
        return True, f"User region updated to {region}"
    
    def user_exists(self, username):
        """Check if user exists"""
        return username in self.users_db
    
    def get_all_users(self):
        """Get all registered users"""
        return list(self.users_db.keys())
    
    def is_logged_in(self):
        """Check if any user is logged in"""
        return self.current_user is not None
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if username not in self.users_db:
            return False, "User not found"
        
        user = self.users_db[username]
        if user['password'] != old_password:
            return False, "Incorrect old password"
        
        if not new_password or len(new_password) < 4:
            return False, "New password must be at least 4 characters"
        
        user['password'] = new_password
        self.save_users()
        return True, "Password changed successfully"
    
    def update_user_info(self, username, email=None, phone=None):
        """Update user information"""
        if username not in self.users_db:
            return False, "User not found"
        
        user = self.users_db[username]
        if email:
            user['email'] = email
        if phone:
            user['phone'] = phone
        
        self.save_users()
        return True, "User information updated"
