"""
Call Management System
Handles actual calling functionality with timers and call tracking
"""

import threading
import time
from datetime import datetime, timedelta


class CallManager:
    """Manages active calls and call state"""
    
    def __init__(self):
        self.active_calls = {}
        self.call_history = []
    
    def start_call(self, call_id, customer_name, astrologer_name, astrologer_phone, duration_minutes):
        """Start a new call"""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        call_data = {
            "call_id": call_id,
            "customer_name": customer_name,
            "astrologer_name": astrologer_name,
            "astrologer_phone": astrologer_phone,
            "duration_minutes": duration_minutes,
            "start_time": start_time,
            "end_time": end_time,
            "elapsed_seconds": 0,
            "status": "active",
            "is_active": True
        }
        
        self.active_calls[call_id] = call_data
        self.call_history.append(call_data)
        return call_data
    
    def end_call(self, call_id):
        """End an active call"""
        if call_id in self.active_calls:
            call = self.active_calls[call_id]
            call["status"] = "completed"
            call["is_active"] = False
            call["actual_end_time"] = datetime.now()
            actual_duration = (call["actual_end_time"] - call["start_time"]).total_seconds() / 60
            call["actual_duration_minutes"] = round(actual_duration, 2)
            del self.active_calls[call_id]
            return call
        return None
    
    def get_call_time_remaining(self, call_id):
        """Get remaining time for a call in seconds"""
        if call_id in self.active_calls:
            call = self.active_calls[call_id]
            time_remaining = (call["end_time"] - datetime.now()).total_seconds()
            return max(0, int(time_remaining))
        return 0
    
    def get_call_elapsed_time(self, call_id):
        """Get elapsed time for a call in seconds"""
        if call_id in self.active_calls:
            call = self.active_calls[call_id]
            elapsed = (datetime.now() - call["start_time"]).total_seconds()
            return max(0, int(elapsed))
        return 0
    
    def is_call_active(self, call_id):
        """Check if a call is still active"""
        return call_id in self.active_calls
    
    def get_active_call(self, call_id):
        """Get active call details"""
        return self.active_calls.get(call_id)
    
    def get_all_active_calls(self):
        """Get all active calls"""
        return self.active_calls
    
    def format_time(self, seconds):
        """Format seconds to MM:SS format"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
