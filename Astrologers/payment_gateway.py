"""
Payment Gateway Integration Module
Simulates payment gateway processing (Stripe, PayPal, UPI)
"""

import re
from datetime import datetime


class PaymentGateway:
    """Simulates payment gateway operations"""
    
    @staticmethod
    def validate_card_number(card_number):
        """Validate card number using Luhn algorithm"""
        card_number = card_number.replace(" ", "").replace("-", "")
        
        if not card_number.isdigit() or len(card_number) != 16:
            return False
        
        # Luhn algorithm
        digits = [int(d) for d in card_number]
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        
        return checksum % 10 == 0
    
    @staticmethod
    def validate_expiry(month, year):
        """Validate card expiry date"""
        try:
            month = int(month)
            year = int(year)
            
            if month < 1 or month > 12:
                return False
            
            current_date = datetime.now()
            expiry_date = datetime(year + 2000, month, 1)
            
            return expiry_date > current_date
        except:
            return False
    
    @staticmethod
    def validate_cvv(cvv):
        """Validate CVV"""
        return cvv.isdigit() and len(cvv) == 3
    
    @staticmethod
    def validate_upi(upi_id):
        """Validate UPI ID format"""
        pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z]+$'
        return re.match(pattern, upi_id) is not None
    
    @staticmethod
    def process_credit_card(card_number, expiry_month, expiry_year, cvv, amount):
        """Process credit card payment"""
        if not PaymentGateway.validate_card_number(card_number):
            return False, "Invalid card number"
        
        if not PaymentGateway.validate_expiry(expiry_month, expiry_year):
            return False, "Card expired or invalid expiry date"
        
        if not PaymentGateway.validate_cvv(cvv):
            return False, "Invalid CVV"
        
        if amount <= 0:
            return False, "Invalid amount"
        
        # Simulate payment processing
        return True, "Payment processed successfully"
    
    @staticmethod
    def process_upi_payment(upi_id, amount):
        """Process UPI payment"""
        if not PaymentGateway.validate_upi(upi_id):
            return False, "Invalid UPI ID"
        
        if amount <= 0:
            return False, "Invalid amount"
        
        # Simulate UPI payment
        return True, "UPI payment processed successfully"
    
    @staticmethod
    def process_paypal_payment(email, amount):
        """Process PayPal payment"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid PayPal email"
        
        if amount <= 0:
            return False, "Invalid amount"
        
        # Simulate PayPal payment
        return True, "PayPal payment processed successfully"
    
    @staticmethod
    def generate_receipt(transaction_id, customer_name, astrologer_name, amount, payment_method, timestamp):
        """Generate payment receipt"""
        receipt = f"""
{'='*50}
                PAYMENT RECEIPT
{'='*50}

Transaction ID: {transaction_id}
Date & Time: {timestamp}

Customer Name: {customer_name}
Astrologer Name: {astrologer_name}
Amount: ₹{amount}
Payment Method: {payment_method}

Status: PAYMENT SUCCESSFUL

{'='*50}
Thank you for using our service!
{'='*50}
        """
        return receipt
