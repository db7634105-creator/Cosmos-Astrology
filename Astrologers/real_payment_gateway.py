"""
Real Payment Gateway Integration
Supports: Khalti, eSewa, PayPal, Stripe
Uses test/sandbox mode for safe testing
"""

import requests
import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple
import qrcode
from io import BytesIO
import base64


class PaymentGateway(Enum):
    """Supported payment gateways"""
    KHALTI = "khalti"
    ESEWA = "esewa"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WALLET = "wallet"


class KhaltiGateway:
    """
    Khalti Payment Gateway Integration (Nepal)
    Test Mode: Uses sandbox API
    Docs: https://docs.khalti.com/
    """
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        if test_mode:
            self.base_url = "https://a.khalti.com/api/v2"
            self.public_key = "test_public_key_dc74e0fd57cb46cd93832722d9d48521"
            self.secret_key = "test_secret_key_dc74e0fd57cb46cd93832722d9d48521"
        else:
            self.base_url = "https://khalti.com/api/v2"
            self.public_key = "your_production_public_key"
            self.secret_key = "your_production_secret_key"
    
    def generate_qr_code(self, phone_number: str, amount: int) -> Tuple[str, str]:
        """
        Generate QR code for Khalti payment
        Returns: (qr_code_base64, transaction_id)
        """
        transaction_id = str(uuid.uuid4())
        qr_data = f"khalti://{phone_number}/{amount}/{transaction_id}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        qr_base64 = base64.b64encode(img_bytes.getvalue()).decode()
        return qr_base64, transaction_id
    
    def initiate_payment(self, amount: int, phone: str, product_name: str) -> Dict:
        """
        Initiate Khalti payment
        Args:
            amount: Amount in paisa (NPR * 100)
            phone: User's phone number
            product_name: Description of product/service
        Returns: Payment response with verification token
        """
        headers = {
            "Authorization": f"Key {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": amount,
            "product_name": product_name,
            "product_identity": str(uuid.uuid4()),
            "success_url": "https://system.cosmosastrology.com/payment/success",
            "failure_url": "https://system.cosmosastrology.com/payment/failure",
            "phone": phone,
            "return_url": "https://system.cosmosastrology.com/payment/return"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/epayment/",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "data": response.json(),
                    "gateway": "khalti"
                }
            else:
                return {
                    "success": False,
                    "error": f"Khalti API Error: {response.text}",
                    "gateway": "khalti"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Khalti Connection Error: {str(e)}",
                "gateway": "khalti"
            }
    
    def verify_payment(self, token: str, amount: int) -> Dict:
        """
        Verify Khalti payment after user completes transaction
        """
        headers = {
            "Authorization": f"Key {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "token": token,
            "amount": amount
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/epayment/complete/",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "gateway": "khalti"
                }
            else:
                return {
                    "success": False,
                    "error": f"Verification failed: {response.text}",
                    "gateway": "khalti"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Verification Error: {str(e)}",
                "gateway": "khalti"
            }


class ESewaGateway:
    """
    eSewa Payment Gateway Integration (Nepal)
    Test Mode: Uses sandbox
    Docs: https://developer.esewa.com.np/
    """
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        if test_mode:
            self.base_url = "https://uat.esewa.com.np"
            self.merchant_code = "EPAYTEST"
            self.merchant_key = "8gBm/:&EnhH.1/q"
        else:
            self.base_url = "https://esewa.com.np"
            self.merchant_code = "your_merchant_code"
            self.merchant_key = "your_merchant_key"
    
    def generate_signature(self, total_amount: float, transaction_uuid: str) -> str:
        """
        Generate eSewa signature for payment
        Uses: total_amount, transaction_uuid, and merchant_key
        """
        import hashlib
        
        message = f"{total_amount}{transaction_uuid}{self.merchant_code}"
        signature = hashlib.md5(message.encode()).hexdigest()
        return signature
    
    def initiate_payment(self, amount: float, email: str, product_name: str) -> Dict:
        """
        Prepare eSewa payment
        Returns: Form data for redirecting to eSewa
        """
        transaction_id = str(uuid.uuid4())
        signature = self.generate_signature(amount, transaction_id)
        
        payment_data = {
            "amt": amount,
            "psc": 0,
            "pdc": 0,
            "txAmt": 0,
            "tAmt": amount,
            "pid": transaction_id,
            "scd": self.merchant_code,
            "su": "https://system.cosmosastrology.com/payment/esewa-success",
            "fu": "https://system.cosmosastrology.com/payment/esewa-failure",
            "signature": signature
        }
        
        return {
            "success": True,
            "payment_url": f"{self.base_url}/epay/main",
            "form_data": payment_data,
            "transaction_id": transaction_id,
            "gateway": "esewa"
        }
    
    def verify_payment(self, transaction_id: str, status: str, ref_id: str) -> Dict:
        """
        Verify eSewa payment using transaction ID
        """
        params = {
            "q": "checkPaymentStatus",
            "rid": ref_id,
            "pid": transaction_id
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/api/bill/epay/checkstatus",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "Complete":
                    return {
                        "success": True,
                        "data": data,
                        "gateway": "esewa"
                    }
            
            return {
                "success": False,
                "error": "Payment verification failed",
                "gateway": "esewa"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"eSewa Verification Error: {str(e)}",
                "gateway": "esewa"
            }


class PayPalGateway:
    """
    PayPal REST API Integration
    Supports: Credit Card, PayPal Wallet, Bank Transfers
    Docs: https://developer.paypal.com/
    """
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        if test_mode:
            self.base_url = "https://api.sandbox.paypal.com"
            self.client_id = "your_sandbox_client_id"
            self.client_secret = "your_sandbox_client_secret"
        else:
            self.base_url = "https://api.paypal.com"
            self.client_id = "your_production_client_id"
            self.client_secret = "your_production_client_secret"
    
    def get_access_token(self) -> Optional[str]:
        """
        Get PayPal OAuth access token
        """
        auth = (self.client_id, self.client_secret)
        headers = {"Accept": "application/json"}
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/oauth2/token",
                auth=auth,
                headers=headers,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("access_token")
        except Exception as e:
            print(f"PayPal Token Error: {e}")
        
        return None
    
    def initiate_payment(self, amount: float, currency: str = "USD", 
                        description: str = "Astrology Consultation") -> Dict:
        """
        Create PayPal payment
        """
        access_token = self.get_access_token()
        if not access_token:
            return {
                "success": False,
                "error": "Could not obtain PayPal access token",
                "gateway": "paypal"
            }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        payload = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [
                {
                    "amount": {
                        "total": str(amount),
                        "currency": currency,
                        "details": {
                            "subtotal": str(amount)
                        }
                    },
                    "description": description,
                    "invoice_number": str(uuid.uuid4())
                }
            ],
            "redirect_urls": {
                "return_url": "https://system.cosmosastrology.com/payment/paypal-success",
                "cancel_url": "https://system.cosmosastrology.com/payment/paypal-cancel"
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/payments/payment",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                approval_url = next(
                    (link["href"] for link in data.get("links", []) 
                     if link["rel"] == "approval_url"),
                    None
                )
                
                return {
                    "success": True,
                    "payment_id": data.get("id"),
                    "approval_url": approval_url,
                    "gateway": "paypal"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"PayPal Error: {str(e)}",
                "gateway": "paypal"
            }
        
        return {
            "success": False,
            "error": "PayPal payment creation failed",
            "gateway": "paypal"
        }
    
    def verify_payment(self, payment_id: str, payer_id: str) -> Dict:
        """
        Execute PayPal payment
        """
        access_token = self.get_access_token()
        if not access_token:
            return {
                "success": False,
                "error": "Could not obtain access token",
                "gateway": "paypal"
            }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        payload = {"payer_id": payer_id}
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/payments/payment/{payment_id}/execute",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "gateway": "paypal"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"PayPal Verification Error: {str(e)}",
                "gateway": "paypal"
            }
        
        return {
            "success": False,
            "error": "PayPal payment verification failed",
            "gateway": "paypal"
        }


class StripeGateway:
    """
    Stripe Payment Processing
    Test Cards: 4242 4242 4242 4242 (success), 4000 0000 0000 0002 (fail)
    """
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        if test_mode:
            self.api_key = "sk_test_your_test_key"
            self.publishable_key = "pk_test_your_test_key"
        else:
            self.api_key = "sk_live_your_live_key"
            self.publishable_key = "pk_live_your_live_key"
    
    def create_payment_intent(self, amount: int, currency: str = "usd") -> Dict:
        """
        Create Stripe payment intent (amount in cents)
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "amount": amount,
            "currency": currency,
            "payment_method_types[]": "card"
        }
        
        try:
            response = requests.post(
                "https://api.stripe.com/v1/payment_intents",
                data=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "client_secret": response.json().get("client_secret"),
                    "gateway": "stripe"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Stripe Error: {str(e)}",
                "gateway": "stripe"
            }
        
        return {
            "success": False,
            "error": "Payment intent creation failed",
            "gateway": "stripe"
        }


class PaymentGatewayFactory:
    """
    Factory for creating payment gateway instances
    """
    
    _gateways = {
        PaymentGateway.KHALTI: KhaltiGateway,
        PaymentGateway.ESEWA: ESewaGateway,
        PaymentGateway.PAYPAL: PayPalGateway,
        PaymentGateway.STRIPE: StripeGateway,
    }
    
    @classmethod
    def create_gateway(cls, gateway_type: PaymentGateway, test_mode: bool = True):
        """
        Create a payment gateway instance
        """
        gateway_class = cls._gateways.get(gateway_type)
        if gateway_class:
            return gateway_class(test_mode=test_mode)
        raise ValueError(f"Unknown gateway: {gateway_type}")
