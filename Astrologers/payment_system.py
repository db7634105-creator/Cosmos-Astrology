"""
Payment System Module
Handles payment processing, transaction management, and wallet functionality
Supports country-specific payment gateways (Nepal: Khalti/Esewa, India: Razorpay)
"""

import json
import os
from datetime import datetime
from enum import Enum
from country_payment_gateway import (
    CountryPaymentGateway, CountryPaymentMapper, PaymentProvider, Country
)


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    WALLET = "wallet"
    PAYPAL = "paypal"


class Transaction:
    def __init__(self, transaction_id, customer_name, astrologer_name, amount, payment_method, 
                 call_duration=0, country=None, payment_provider=None):
        self.transaction_id = transaction_id
        self.customer_name = customer_name
        self.astrologer_name = astrologer_name
        self.amount = amount
        self.payment_method = payment_method
        self.country = country or "others"
        self.payment_provider = payment_provider or "card"
        self.status = PaymentStatus.PENDING
        self.call_duration = call_duration  # in minutes
        self.timestamp = datetime.now()
        self.description = f"Call with {astrologer_name}"
    
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "customer_name": self.customer_name,
            "astrologer_name": self.astrologer_name,
            "amount": self.amount,
            "payment_method": self.payment_method.value if hasattr(self.payment_method, 'value') else str(self.payment_method),
            "country": self.country,
            "payment_provider": self.payment_provider,
            "status": self.status.value,
            "call_duration": self.call_duration,
            "timestamp": self.timestamp.isoformat(),
            "description": self.description
        }


class PaymentSystem:
    def __init__(self, data_file="transactions.json"):
        self.data_file = data_file
        self.transactions = []
        self.wallet_balance = {}
        self.load_transactions()
    
    def load_transactions(self):
        """Load transactions from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = data.get('transactions', [])
                    self.wallet_balance = data.get('wallet_balance', {})
            except:
                self.transactions = []
                self.wallet_balance = {}
        else:
            self.transactions = []
            self.wallet_balance = {}
    
    def save_transactions(self):
        """Save transactions to file"""
        data = {
            'transactions': self.transactions,
            'wallet_balance': self.wallet_balance
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4, default=str)
    
    def create_transaction(self, customer_name, astrologer_name, amount, payment_method, 
                          call_duration=0, country=None, payment_provider=None):
        """Create a new transaction with country-specific payment provider"""
        transaction_id = f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.transactions)}"
        transaction = Transaction(transaction_id, customer_name, astrologer_name, amount, 
                                 payment_method, call_duration, country, payment_provider)
        return transaction
    
    def process_payment(self, transaction, card_details=None, upi_id=None, phone_number=None, email=None):
        """Process payment transaction with country-specific gateway routing"""
        try:
            # Validate transaction
            if transaction.amount <= 0:
                transaction.status = PaymentStatus.FAILED
                return False, "Invalid amount"
            
            # Check wallet balance if paying via wallet
            if transaction.payment_method == PaymentMethod.WALLET:
                customer_balance = self.wallet_balance.get(transaction.customer_name, 0)
                if customer_balance < transaction.amount:
                    transaction.status = PaymentStatus.FAILED
                    return False, "Insufficient wallet balance"
                self.wallet_balance[transaction.customer_name] = customer_balance - transaction.amount
                transaction.status = PaymentStatus.COMPLETED
                self.transactions.append(transaction.to_dict())
                self.save_transactions()
                return True, f"Wallet payment successful. Transaction ID: {transaction.transaction_id}"
            
            # Process country-specific payment
            country = CountryPaymentMapper.get_country_from_region(transaction.country)
            payment_provider = transaction.payment_provider or str(CountryPaymentMapper.get_default_provider(country).value)
            
            # Prepare payment parameters
            payment_kwargs = {
                'phone_number': phone_number,
                'email': email,
                'upi_id': upi_id,
                'payment_method': 'upi' if upi_id else 'phone' if phone_number else 'card'
            }
            
            # Route payment to country-specific gateway
            success, message = CountryPaymentGateway.process_payment(
                country, 
                payment_provider, 
                transaction.amount, 
                transaction.transaction_id,
                **payment_kwargs
            )
            
            if success:
                transaction.status = PaymentStatus.COMPLETED
                self.transactions.append(transaction.to_dict())
                self.save_transactions()
                return True, f"{message}. Payment successful!"
            else:
                transaction.status = PaymentStatus.FAILED
                return False, f"Payment failed: {message}"
        
        except Exception as e:
            transaction.status = PaymentStatus.FAILED
            return False, f"Payment processing error: {str(e)}"
    
    def validate_payment_method(self, method, card_details=None, upi_id=None):
        """Validate payment method details"""
        if method == PaymentMethod.CREDIT_CARD or method == PaymentMethod.DEBIT_CARD:
            if not card_details:
                return False
            card_number = card_details.get('card_number', '').replace(' ', '')
            cvv = card_details.get('cvv', '')
            if len(card_number) != 16 or len(cvv) != 3:
                return False
            return True
        
        elif method == PaymentMethod.UPI:
            if not upi_id:
                return False
            return '@' in upi_id
        
        elif method == PaymentMethod.WALLET:
            return True
        
        elif method == PaymentMethod.PAYPAL:
            return True
        
        return False
    
    def add_to_wallet(self, customer_name, amount):
        """Add money to customer wallet"""
        if amount <= 0:
            return False, "Invalid amount"
        
        current_balance = self.wallet_balance.get(customer_name, 0)
        self.wallet_balance[customer_name] = current_balance + amount
        self.save_transactions()
        return True, f"Added ₹{amount} to wallet. New balance: ₹{self.wallet_balance[customer_name]}"
    
    def get_wallet_balance(self, customer_name):
        """Get customer wallet balance"""
        return self.wallet_balance.get(customer_name, 0)
    
    def refund_transaction(self, transaction_id):
        """Refund a transaction"""
        for txn in self.transactions:
            if txn['transaction_id'] == transaction_id:
                if txn['status'] == 'completed':
                    txn['status'] = 'refunded'
                    # Add refund amount back to wallet
                    customer_name = txn['customer_name']
                    current_balance = self.wallet_balance.get(customer_name, 0)
                    self.wallet_balance[customer_name] = current_balance + txn['amount']
                    self.save_transactions()
                    return True, "Refund processed successfully"
                else:
                    return False, "Can only refund completed transactions"
        
        return False, "Transaction not found"
    
    def get_transaction_history(self, customer_name=None):
        """Get transaction history"""
        if customer_name:
            return [t for t in self.transactions if t['customer_name'] == customer_name]
        return self.transactions
    
    def get_astrologer_earnings(self, astrologer_name):
        """Get total earnings for an astrologer"""
        total = sum(t['amount'] for t in self.transactions 
                   if t['astrologer_name'] == astrologer_name and t['status'] == 'completed')
        return total
    
    def get_pricing_tiers(self):
        """Get available pricing tiers for consultations"""
        return {
            "5_min": {"duration": 5, "price": 99},
            "15_min": {"duration": 15, "price": 249},
            "30_min": {"duration": 30, "price": 449},
            "60_min": {"duration": 60, "price": 799}
        }
    
    def get_available_payment_providers(self, country):
        """Get available payment providers for a specific country"""
        country_enum = CountryPaymentMapper.get_country_from_region(country)
        providers = CountryPaymentMapper.get_available_providers(country_enum)
        
        return {
            "country": country,
            "providers": [
                {
                    "name": p.value,
                    "details": CountryPaymentGateway.get_payment_instructions(country_enum, p)
                }
                for p in providers
            ]
        }
    
    def get_default_payment_provider(self, country):
        """Get the default payment provider for a country"""
        country_enum = CountryPaymentMapper.get_country_from_region(country)
        provider = CountryPaymentMapper.get_default_provider(country_enum)
        return {
            "provider": provider.value,
            "details": CountryPaymentGateway.get_payment_instructions(country_enum, provider)
        }
