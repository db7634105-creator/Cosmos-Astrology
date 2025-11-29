"""
Call Handler Module
Handles phone calls to astrologers
"""

import webbrowser
from datetime import datetime


def make_call(phone_number, astrologer_name):
    """
    Simulate a phone call to the astrologer.
    In a real application, this would integrate with a VoIP service.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*60}")
    print(f"[{timestamp}] Initiating call to {astrologer_name}")
    print(f"Phone Number: {phone_number}")
    print(f"{'='*60}\n")
    
    # Try to open the phone dialer (Windows)
    try:
        webbrowser.open(f"tel:{phone_number}")
        return True, f"Calling {astrologer_name}..."
    except Exception as e:
        # Fallback if tel: protocol is not supported
        return False, f"Could not initiate call. Error: {str(e)}"


def log_call_history(astrologer_name, phone_number):
    """
    Log the call history to a file
    """
    try:
        with open("call_history.log", "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - Called {astrologer_name} ({phone_number})\n")
    except Exception as e:
        print(f"Error logging call: {str(e)}")
