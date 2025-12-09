"""
WhatsApp Calling Integration
Supports WhatsApp calling after successful payment
Two approaches:
1. Direct WhatsApp Link (user clicks)
2. Twilio Integration (for automated calls)
"""

import webbrowser
import urllib.parse
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import json


class WhatsAppCaller:
    """
    WhatsApp calling integration
    Handles direct calls and call scheduling
    """
    
    def __init__(self):
        self.call_history = []
        self.pending_calls = []
    
    def generate_whatsapp_link(self, phone_number: str, 
                               astrologer_name: str,
                               message: str = "") -> str:
        """
        Generate WhatsApp chat link
        Phone format: 977XXXXXXXXXX (country code + number)
        """
        if not phone_number.startswith("+"):
            # Add country code if missing
            if not phone_number.startswith("977"):
                phone_number = "+977" + phone_number
            else:
                phone_number = "+" + phone_number
        
        default_message = f"Hi {astrologer_name}, I have booked a consultation with you. Please call me on WhatsApp."
        
        if message:
            full_message = f"{message}\n\n{default_message}"
        else:
            full_message = default_message
        
        # URL encode the message
        encoded_message = urllib.parse.quote(full_message)
        
        # Create WhatsApp link
        whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"
        
        return whatsapp_url
    
    def initiate_whatsapp_call(self, phone_number: str, 
                              astrologer_name: str,
                              duration_minutes: int = 30,
                              message: str = "") -> Dict:
        """
        Initiate WhatsApp call by opening browser link
        User manually initiates call from WhatsApp
        
        Args:
            phone_number: Astrologer's WhatsApp number
            astrologer_name: Name of astrologer
            duration_minutes: Scheduled call duration
            message: Custom message to send first
        
        Returns: Call initiation response
        """
        try:
            whatsapp_link = self.generate_whatsapp_link(
                phone_number, 
                astrologer_name,
                message
            )
            
            # Open WhatsApp in browser
            webbrowser.open(whatsapp_link)
            
            call_record = {
                "timestamp": datetime.now().isoformat(),
                "astrologer": astrologer_name,
                "phone": phone_number,
                "duration_minutes": duration_minutes,
                "status": "initiated",
                "method": "whatsapp_link"
            }
            
            self.call_history.append(call_record)
            
            return {
                "success": True,
                "message": f"WhatsApp opened. Please call {astrologer_name}",
                "call_link": whatsapp_link,
                "call_record": call_record
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"WhatsApp initiation failed: {str(e)}"
            }
    
    def schedule_whatsapp_call(self, phone_number: str,
                               astrologer_name: str,
                               scheduled_time: datetime,
                               duration_minutes: int = 30) -> Dict:
        """
        Schedule a WhatsApp call for later
        """
        try:
            call_record = {
                "timestamp": datetime.now().isoformat(),
                "scheduled_time": scheduled_time.isoformat(),
                "astrologer": astrologer_name,
                "phone": phone_number,
                "duration_minutes": duration_minutes,
                "status": "scheduled",
                "reminder_sent": False
            }
            
            self.pending_calls.append(call_record)
            
            return {
                "success": True,
                "message": f"Call scheduled with {astrologer_name} at {scheduled_time}",
                "call_record": call_record
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Call scheduling failed: {str(e)}"
            }
    
    def get_call_history(self) -> list:
        """Get list of all calls made"""
        return self.call_history
    
    def get_pending_calls(self) -> list:
        """Get list of scheduled pending calls"""
        return self.pending_calls


class TwilioWhatsAppCaller:
    """
    Twilio-based WhatsApp calling
    Requires: Twilio account with WhatsApp sandbox
    More automated but requires API keys
    """
    
    def __init__(self, account_sid: str = "", auth_token: str = "", 
                 twilio_whatsapp_number: str = ""):
        """
        Initialize Twilio WhatsApp caller
        
        Get these from: https://www.twilio.com/console
        WhatsApp: https://www.twilio.com/console/sms/whatsapp/learn
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_whatsapp_number = twilio_whatsapp_number  # e.g., "+1234567890"
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}"
    
    def send_whatsapp_notification(self, recipient_number: str,
                                   message: str) -> Dict:
        """
        Send WhatsApp message via Twilio
        Requires sandbox setup
        """
        if not all([self.account_sid, self.auth_token, self.twilio_whatsapp_number]):
            return {
                "success": False,
                "error": "Twilio credentials not configured. Using manual WhatsApp instead."
            }
        
        try:
            import requests
            from requests.auth import HTTPBasicAuth
            
            url = f"{self.base_url}/Messages.json"
            
            payload = {
                "From": f"whatsapp:{self.twilio_whatsapp_number}",
                "To": f"whatsapp:{recipient_number}",
                "Body": message
            }
            
            response = requests.post(
                url,
                data=payload,
                auth=HTTPBasicAuth(self.account_sid, self.auth_token),
                timeout=10
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "message_id": response.json().get("sid"),
                    "message": "WhatsApp notification sent"
                }
            else:
                return {
                    "success": False,
                    "error": f"Twilio error: {response.text}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Twilio connection error: {str(e)}"
            }
    
    def initiate_call(self, recipient_number: str,
                     astrologer_name: str) -> Dict:
        """
        Initiate WhatsApp call via Twilio
        Note: Direct calling via Twilio WhatsApp is limited
        Sending notification message instead
        """
        message = (
            f"Hi! Your scheduled call with {astrologer_name} is starting now. "
            f"Please click the call button to connect on WhatsApp."
        )
        
        return self.send_whatsapp_notification(recipient_number, message)


class CallScheduler:
    """
    Manages scheduled calls and reminders
    """
    
    def __init__(self):
        self.scheduled_calls = {}
    
    def add_scheduled_call(self, call_id: str, call_time: datetime,
                          phone_number: str, astrologer_name: str,
                          duration_minutes: int) -> Dict:
        """
        Add a call to schedule
        """
        self.scheduled_calls[call_id] = {
            "call_time": call_time,
            "phone": phone_number,
            "astrologer": astrologer_name,
            "duration": duration_minutes,
            "reminder_15min_sent": False,
            "reminder_5min_sent": False,
            "call_initiated": False
        }
        
        return {
            "success": True,
            "call_id": call_id,
            "scheduled_time": call_time.isoformat()
        }
    
    def get_due_reminders(self) -> list:
        """
        Get calls that need reminders
        Returns: List of call IDs needing 15-min or 5-min reminders
        """
        now = datetime.now()
        due_reminders = []
        
        for call_id, call_data in self.scheduled_calls.items():
            time_until_call = call_data["call_time"] - now
            
            # 15-minute reminder
            if (time_until_call.total_seconds() <= 900 and
                not call_data["reminder_15min_sent"]):
                due_reminders.append({
                    "call_id": call_id,
                    "type": "15min",
                    "call_data": call_data
                })
                call_data["reminder_15min_sent"] = True
            
            # 5-minute reminder
            elif (time_until_call.total_seconds() <= 300 and
                  not call_data["reminder_5min_sent"]):
                due_reminders.append({
                    "call_id": call_id,
                    "type": "5min",
                    "call_data": call_data
                })
                call_data["reminder_5min_sent"] = True
        
        return due_reminders
    
    def initiate_due_call(self, call_id: str) -> Dict:
        """
        Initiate a call that's due
        """
        if call_id not in self.scheduled_calls:
            return {
                "success": False,
                "error": "Call not found"
            }
        
        call_data = self.scheduled_calls[call_id]
        now = datetime.now()
        
        if now >= call_data["call_time"]:
            call_data["call_initiated"] = True
            
            caller = WhatsAppCaller()
            return caller.initiate_whatsapp_call(
                call_data["phone"],
                call_data["astrologer"],
                call_data["duration"]
            )
        
        return {
            "success": False,
            "error": "Call time has not arrived yet"
        }
