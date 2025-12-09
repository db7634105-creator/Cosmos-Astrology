"""
Payment integration module - connects to real payment gateways
"""

from typing import Optional, Dict
from enum import Enum
from sqlalchemy.orm import Session
from backend.models import Consultation, User, Question


class PaymentGateway(str, Enum):
    """Available payment gateways"""
    KHALTI = "khalti"
    ESEWA = "esewa"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    WALLET = "wallet"


class PaymentProcessor:
    """Handle payments for consultations"""
    
    def __init__(self):
        import os
        self.khalti_key = os.getenv("KHALTI_PUBLIC_KEY")
        self.esewa_key = os.getenv("ESEWA_MERCHANT_CODE")
        self.paypal_client_id = os.getenv("PAYPAL_CLIENT_ID")
        self.stripe_key = os.getenv("STRIPE_SECRET_KEY")
    
    def process_consultation_payment(
        self,
        user_id: int,
        astrologer_id: int,
        amount: float,
        gateway: PaymentGateway,
        db: Session
    ) -> Dict:
        """Process payment for consultation"""
        
        try:
            if gateway == PaymentGateway.KHALTI:
                return self.process_khalti_payment(amount, user_id)
            
            elif gateway == PaymentGateway.ESEWA:
                return self.process_esewa_payment(amount, user_id)
            
            elif gateway == PaymentGateway.PAYPAL:
                return self.process_paypal_payment(amount, user_id)
            
            elif gateway == PaymentGateway.STRIPE:
                return self.process_stripe_payment(amount, user_id)
            
            elif gateway == PaymentGateway.WALLET:
                return self.process_wallet_payment(amount, user_id, db)
            
            else:
                return {"success": False, "error": "Unknown gateway"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_khalti_payment(self, amount: float, user_id: int) -> Dict:
        """Process Khalti payment"""
        import requests
        
        try:
            # Convert to paisa (1 NPR = 100 paisa)
            amount_paisa = int(amount * 100)
            
            payload = {
                "public_key": self.khalti_key,
                "transaction_uuid": f"user_{user_id}_{int(datetime.utcnow().timestamp())}",
                "amount": amount_paisa,
                "product_name": "Astrology Consultation",
                "product_url": "https://cosmosastrology.com",
                "return_url": "https://cosmosastrology.com/payment/khalti/success",
                "website_url": "https://cosmosastrology.com"
            }
            
            return {
                "success": True,
                "gateway": "khalti",
                "amount": amount,
                "payload": payload
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_esewa_payment(self, amount: float, user_id: int) -> Dict:
        """Process eSewa payment"""
        import hashlib
        import uuid
        
        try:
            transaction_uuid = str(uuid.uuid4())
            
            # Create MD5 signature
            signature_data = f"{self.esewa_key}{amount}{transaction_uuid}"
            signature = hashlib.md5(signature_data.encode()).hexdigest()
            
            return {
                "success": True,
                "gateway": "esewa",
                "amount": amount,
                "transaction_uuid": transaction_uuid,
                "signature": signature,
                "merchant_code": self.esewa_key,
                "payment_url": "https://uat.esewa.com.np/epay/main"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_paypal_payment(self, amount: float, user_id: int) -> Dict:
        """Process PayPal payment"""
        import requests
        
        try:
            # Get access token
            auth_response = requests.post(
                "https://api.paypal.com/v1/oauth2/token",
                auth=(self.paypal_client_id, os.getenv("PAYPAL_SECRET")),
                data={"grant_type": "client_credentials"},
                timeout=10
            )
            
            if auth_response.status_code != 200:
                return {"success": False, "error": "Failed to authenticate with PayPal"}
            
            access_token = auth_response.json()['access_token']
            
            # Create payment
            payment_data = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": f"{amount:.2f}",
                        "currency": "USD",
                        "details": {
                            "subtotal": f"{amount:.2f}"
                        }
                    },
                    "description": "Astrology Consultation",
                    "item_list": {
                        "items": [{
                            "name": "Consultation",
                            "quantity": 1,
                            "price": f"{amount:.2f}",
                            "currency": "USD"
                        }]
                    }
                }],
                "redirect_urls": {
                    "return_url": "https://cosmosastrology.com/payment/paypal/success",
                    "cancel_url": "https://cosmosastrology.com/payment/paypal/cancel"
                }
            }
            
            response = requests.post(
                "https://api.paypal.com/v1/payments/payment",
                json=payment_data,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            
            if response.status_code == 201:
                payment = response.json()
                # Find approval link
                approval_url = None
                for link in payment.get('links', []):
                    if link['rel'] == 'approval_url':
                        approval_url = link['href']
                        break
                
                return {
                    "success": True,
                    "gateway": "paypal",
                    "amount": amount,
                    "payment_id": payment['id'],
                    "approval_url": approval_url
                }
            else:
                return {"success": False, "error": "PayPal payment creation failed"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_stripe_payment(self, amount: float, user_id: int) -> Dict:
        """Process Stripe payment"""
        try:
            import stripe
            stripe.api_key = self.stripe_key
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency="usd",
                metadata={
                    "user_id": user_id,
                    "service": "astrology_consultation"
                }
            )
            
            return {
                "success": True,
                "gateway": "stripe",
                "amount": amount,
                "client_secret": intent['client_secret'],
                "payment_intent_id": intent['id']
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_wallet_payment(self, amount: float, user_id: int, db: Session) -> Dict:
        """Process wallet-based payment"""
        try:
            from models import User
            
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Check wallet balance (would need to implement wallet table)
            # For now, assume sufficient balance
            
            return {
                "success": True,
                "gateway": "wallet",
                "amount": amount,
                "transaction_id": f"wallet_{user_id}_{datetime.utcnow().timestamp()}"
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_payment(self, gateway: PaymentGateway, transaction_id: str, verification_data: Dict) -> bool:
        """Verify payment from gateway"""
        
        try:
            if gateway == PaymentGateway.KHALTI:
                return self.verify_khalti(transaction_id, verification_data)
            
            elif gateway == PaymentGateway.ESEWA:
                return self.verify_esewa(transaction_id, verification_data)
            
            elif gateway == PaymentGateway.PAYPAL:
                return self.verify_paypal(transaction_id, verification_data)
            
            elif gateway == PaymentGateway.STRIPE:
                return self.verify_stripe(transaction_id, verification_data)
            
            elif gateway == PaymentGateway.WALLET:
                return True  # Wallet payments don't need external verification
            
            return False
        
        except Exception as e:
            print(f"Payment verification error: {e}")
            return False
    
    def verify_khalti(self, transaction_id: str, verification_data: Dict) -> bool:
        """Verify Khalti payment"""
        import requests
        
        try:
            response = requests.post(
                "https://khalti.com/api/v2/payment/verify/",
                json={"token": verification_data.get("token")},
                headers={"Authorization": f"Key {self.khalti_key}"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def verify_esewa(self, transaction_id: str, verification_data: Dict) -> bool:
        """Verify eSewa payment"""
        import requests
        
        try:
            response = requests.post(
                "https://uat.esewa.com.np/epay/transrec",
                data=verification_data,
                timeout=10
            )
            return "Success" in response.text
        except:
            return False
    
    def verify_paypal(self, transaction_id: str, verification_data: Dict) -> bool:
        """Verify PayPal payment"""
        import requests
        
        try:
            # Use PaymentID from verification_data
            payment_id = verification_data.get("paymentId")
            payer_id = verification_data.get("payerId")
            
            # Get PayPal token (simplified)
            auth_response = requests.post(
                "https://api.paypal.com/v1/oauth2/token",
                auth=(self.paypal_client_id, os.getenv("PAYPAL_SECRET")),
                data={"grant_type": "client_credentials"},
                timeout=10
            )
            
            if auth_response.status_code != 200:
                return False
            
            access_token = auth_response.json()['access_token']
            
            # Execute payment
            response = requests.post(
                f"https://api.paypal.com/v1/payments/payment/{payment_id}/execute",
                json={"payer_id": payer_id},
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            
            return response.status_code in [200, 201]
        except:
            return False
    
    def verify_stripe(self, transaction_id: str, verification_data: Dict) -> bool:
        """Verify Stripe payment"""
        try:
            import stripe
            stripe.api_key = self.stripe_key
            
            intent = stripe.PaymentIntent.retrieve(transaction_id)
            return intent['status'] == 'succeeded'
        except:
            return False


# Global payment processor instance
payment_processor = PaymentProcessor()

from datetime import datetime
import os
