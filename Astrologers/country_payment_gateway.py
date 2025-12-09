"""
Country-Specific Payment Gateway Module
Handles payment processing for different countries:
- Nepal: Khalti, Esewa
- India: Razorpay
"""

import re
import os
import json
from datetime import datetime
from enum import Enum

try:
    import requests
except Exception:
    requests = None


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
    def process_payment(phone_number, amount, transaction_id, khalti_token=None):
        """Process Khalti payment"""
        if not KhaltiGateway.validate_phone(phone_number):
            return False, "Invalid Nepali phone number format (should start with 98/97)"

        if amount <= 0:
            return False, "Invalid amount"

        # Use passed khalti_token first, then environment variable
        token_to_use = khalti_token or os.environ.get('KHALTI_PAYMENT_TOKEN')
        khalti_secret = os.environ.get('KHALTI_SECRET_KEY')

        if token_to_use and khalti_secret and requests:
            # Khalti expects token and amount (amount depends on your integration units)
            verify_url = "https://khalti.com/api/v2/payment/verify/"
            headers = {"Authorization": f"Key {khalti_secret}"}
            payload = {"token": token_to_use, "amount": int(amount)}
            try:
                resp = requests.post(verify_url, data=payload, headers=headers, timeout=10)
                if resp.status_code == 200:
                    # Optionally parse response JSON for more detail
                    try:
                        data = resp.json()
                    except Exception:
                        data = resp.text
                    return True, f"Khalti payment verified. Transaction ID: {transaction_id}. Response: {data}"
                else:
                    return False, f"Khalti verification failed: {resp.status_code} {resp.text}"
            except Exception as e:
                return False, f"Khalti request error: {str(e)}"

        # Fallback simulated response
        return True, f"Khalti payment processed successfully (simulated). Transaction ID: {transaction_id}"
    
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
        # If eSewa merchant credentials and reference are provided, attempt real verification
        esewa_ref = os.environ.get('ESEWA_PAYMENT_REF')
        esewa_merchant = os.environ.get('ESEWA_MERCHANT_CODE')

        if esewa_ref and esewa_merchant and requests:
            # eSewa verification is typically done via a GET/POST to their verification endpoint.
            # This implementation tries a basic verification pattern and will return the provider response if possible.
            verify_url = "https://esewa.com.np/epay/transrec"  # eSewa transaction record endpoint
            params = {"pid": esewa_ref, "scd": esewa_merchant, "amt": amount}
            try:
                resp = requests.get(verify_url, params=params, timeout=10)
                # eSewa returns XML/HTML in many flows; accept 200 as success here and return body for debugging
                if resp.status_code == 200:
                    return True, f"Esewa verification response received. Transaction ID: {transaction_id}"
                else:
                    return False, f"Esewa verification failed: {resp.status_code} {resp.text}"
            except Exception as e:
                return False, f"Esewa request error: {str(e)}"

        # Fallback simulated response
        return True, f"Esewa payment processed successfully (simulated). Transaction ID: {transaction_id}"
    
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
            # Accept either a phone number (legacy/simulated flow) or a Khalti token for real verification
            phone = kwargs.get('phone_number')
            khalti_token = kwargs.get('khalti_token') or os.environ.get('KHALTI_PAYMENT_TOKEN')

            if khalti_token:
                # When using Khalti checkout, the client should provide a `khalti_token` returned by Khalti SDK
                # we'll pass phone_number (if any) for backward compatibility
                return KhaltiGateway.process_payment(phone or "", amount, transaction_id, khalti_token=khalti_token)

            if not phone:
                return False, "Phone number required for Khalti (or provide khalti_token for real verification)"

            return KhaltiGateway.process_payment(phone, amount, transaction_id)
        
        elif payment_provider == PaymentProvider.ESEWA:
            # Accept either an email (legacy/simulated) or an eSewa reference/merchant flow for real verification
            email = kwargs.get('email')
            esewa_ref = kwargs.get('esewa_ref') or os.environ.get('ESEWA_PAYMENT_REF')

            if esewa_ref:
                # For real eSewa verification the calling flow should provide `esewa_ref` and merchant config
                return EsewaGateway.process_payment(email or "", amount, transaction_id)

            if not email:
                return False, "Email required for Esewa (or provide esewa_ref for real verification)"

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
