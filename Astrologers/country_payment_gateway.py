"""
Country-Specific Payment Gateway Module
Handles payment processing for different countries:
- Nepal: Khalti, Esewa
- India: Razorpay
"""

import re
from datetime import datetime
from enum import Enum


class Country(Enum):
    NEPAL = "nepal"
    INDIA = "india"
    OTHERS = "others"


class PaymentProvider(Enum):
    # Nepal providers
    KHALTI = "khalti"
    ESEWA = "esewa"
    
    # India providers
    RAZORPAY = "razorpay"
    
    # Fallback
    CARD = "card"
    PAYPAL = "paypal"


class CountryPaymentMapper:
    """Maps countries to available payment providers"""
    
    COUNTRY_PROVIDERS = {
        Country.NEPAL: [PaymentProvider.KHALTI, PaymentProvider.ESEWA],
        Country.INDIA: [PaymentProvider.RAZORPAY],
        Country.OTHERS: [PaymentProvider.CARD, PaymentProvider.PAYPAL]
    }
    
    @staticmethod
    def get_country_from_region(region):
        """Convert region string to Country enum"""
        region_lower = region.lower() if region else "others"
        
        if "nepal" in region_lower:
            return Country.NEPAL
        elif "india" in region_lower:
            return Country.INDIA
        else:
            return Country.OTHERS
    
    @staticmethod
    def get_available_providers(country):
        """Get available payment providers for a country"""
        return CountryPaymentMapper.COUNTRY_PROVIDERS.get(country, 
                                                          CountryPaymentMapper.COUNTRY_PROVIDERS[Country.OTHERS])
    
    @staticmethod
    def get_default_provider(country):
        """Get the default payment provider for a country"""
        providers = CountryPaymentMapper.get_available_providers(country)
        return providers[0] if providers else PaymentProvider.CARD


class KhaltiGateway:
    """Khalti Payment Gateway for Nepal"""
    
    @staticmethod
    def validate_phone(phone_number):
        """Validate Nepali phone number format (10 digits, starts with 98 or 97)"""
        phone = phone_number.replace(" ", "").replace("-", "")
        pattern = r'^(98|97)\d{8}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def process_payment(phone_number, amount, transaction_id):
        """Process Khalti payment"""
        if not KhaltiGateway.validate_phone(phone_number):
            return False, "Invalid Nepali phone number format (should start with 98/97)"
        
        if amount <= 0:
            return False, "Invalid amount"
        
        # Simulate Khalti API call
        return True, f"Khalti payment processed successfully. Transaction ID: {transaction_id}"
    
    @staticmethod
    def validate_khalti_id(khalti_id):
        """Validate Khalti merchant ID or wallet ID"""
        return khalti_id and len(khalti_id) >= 5


class EsewaGateway:
    """Esewa Payment Gateway for Nepal"""
    
    @staticmethod
    def validate_email(email):
        """Validate email for Esewa"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def process_payment(email, amount, transaction_id):
        """Process Esewa payment"""
        if not EsewaGateway.validate_email(email):
            return False, "Invalid email for Esewa"
        
        if amount <= 0:
            return False, "Invalid amount"
        
        # Simulate Esewa API call
        return True, f"Esewa payment processed successfully. Transaction ID: {transaction_id}"
    
    @staticmethod
    def validate_merchant_code(merchant_code):
        """Validate Esewa merchant code"""
        return merchant_code and len(merchant_code) >= 5


class RazorpayGateway:
    """Razorpay Payment Gateway for India"""
    
    @staticmethod
    def validate_phone(phone_number):
        """Validate Indian phone number (10 digits, starts with 6-9)"""
        phone = phone_number.replace(" ", "").replace("-", "")
        pattern = r'^[6-9]\d{9}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_upi(upi_id):
        """Validate Indian UPI ID format"""
        pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z]+$'
        return re.match(pattern, upi_id) is not None
    
    @staticmethod
    def process_payment(payment_method, amount, transaction_id, phone_or_upi=None):
        """Process Razorpay payment
        
        Args:
            payment_method: 'upi', 'card', or 'phone'
            amount: Payment amount
            transaction_id: Unique transaction ID
            phone_or_upi: Phone number or UPI ID
        """
        if amount <= 0:
            return False, "Invalid amount"
        
        if payment_method.lower() == "upi":
            if not RazorpayGateway.validate_upi(phone_or_upi):
                return False, "Invalid UPI ID format"
            return True, f"Razorpay UPI payment processed successfully. Transaction ID: {transaction_id}"
        
        elif payment_method.lower() == "phone":
            if not RazorpayGateway.validate_phone(phone_or_upi):
                return False, "Invalid Indian phone number"
            return True, f"Razorpay phone payment processed successfully. Transaction ID: {transaction_id}"
        
        elif payment_method.lower() == "card":
            return True, f"Razorpay card payment processed successfully. Transaction ID: {transaction_id}"
        
        return False, "Invalid payment method"
    
    @staticmethod
    def validate_merchant_key(merchant_key):
        """Validate Razorpay merchant key"""
        return merchant_key and len(merchant_key) >= 10


class CountryPaymentGateway:
    """Main gateway that routes to country-specific providers"""
    
    @staticmethod
    def process_payment(country, payment_provider, amount, transaction_id, **kwargs):
        """
        Process payment based on country and provider
        
        Args:
            country: Country enum or string
            payment_provider: PaymentProvider enum or string
            amount: Payment amount
            transaction_id: Unique transaction ID
            **kwargs: Additional parameters specific to payment provider
                - For Khalti: phone_number
                - For Esewa: email
                - For Razorpay: upi_id or phone_number or payment_method
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if isinstance(country, str):
            country = CountryPaymentMapper.get_country_from_region(country)
        
        if isinstance(payment_provider, str):
            payment_provider = PaymentProvider(payment_provider.lower())
        
        # Route to appropriate payment gateway
        if payment_provider == PaymentProvider.KHALTI:
            phone = kwargs.get('phone_number')
            if not phone:
                return False, "Phone number required for Khalti"
            return KhaltiGateway.process_payment(phone, amount, transaction_id)
        
        elif payment_provider == PaymentProvider.ESEWA:
            email = kwargs.get('email')
            if not email:
                return False, "Email required for Esewa"
            return EsewaGateway.process_payment(email, amount, transaction_id)
        
        elif payment_provider == PaymentProvider.RAZORPAY:
            upi_id = kwargs.get('upi_id')
            phone = kwargs.get('phone_number')
            payment_method = kwargs.get('payment_method', 'upi' if upi_id else 'phone')
            
            if payment_method == 'upi' and not upi_id:
                return False, "UPI ID required for Razorpay UPI payment"
            elif payment_method == 'phone' and not phone:
                return False, "Phone number required for Razorpay phone payment"
            
            return RazorpayGateway.process_payment(payment_method, amount, transaction_id, 
                                                   phone_or_upi=upi_id or phone)
        
        else:
            return False, "Payment provider not supported for this country"
    
    @staticmethod
    def get_payment_instructions(country, payment_provider):
        """Get payment instructions for a specific provider"""
        instructions = {
            PaymentProvider.KHALTI: {
                "name": "Khalti",
                "country": "Nepal",
                "description": "Khalti is a leading digital wallet in Nepal",
                "supported_methods": ["Phone Number"],
                "instruction": "Enter your registered Khalti phone number"
            },
            PaymentProvider.ESEWA: {
                "name": "Esewa",
                "country": "Nepal",
                "description": "Esewa is a digital payment service in Nepal",
                "supported_methods": ["Email"],
                "instruction": "Enter your registered Esewa email address"
            },
            PaymentProvider.RAZORPAY: {
                "name": "Razorpay",
                "country": "India",
                "description": "Razorpay is India's leading payment platform",
                "supported_methods": ["UPI", "Phone", "Card"],
                "instruction": "Choose your preferred payment method: UPI, Phone, or Card"
            },
            PaymentProvider.CARD: {
                "name": "Credit/Debit Card",
                "country": "International",
                "description": "Pay using Credit or Debit Card",
                "supported_methods": ["Credit Card", "Debit Card"],
                "instruction": "Enter your card details"
            },
            PaymentProvider.PAYPAL: {
                "name": "PayPal",
                "country": "International",
                "description": "Pay using PayPal",
                "supported_methods": ["PayPal Wallet"],
                "instruction": "Authenticate with your PayPal account"
            }
        }
        
        return instructions.get(payment_provider, {
            "name": "Unknown",
            "country": "Unknown",
            "description": "Unknown payment method"
        })
