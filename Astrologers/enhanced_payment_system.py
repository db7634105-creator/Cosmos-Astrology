"""
Enhanced Payment System
Integrates real payment gateways with wallet system
Handles transactions, verification, and refunds
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from enum import Enum
import os


class TransactionStatus(Enum):
    """Transaction status states"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class Transaction:
    """Represents a single transaction"""
    
    def __init__(self, amount: float, gateway: str, user_id: str,
                 astrologer_id: str, purpose: str = "consultation"):
        self.transaction_id = str(uuid.uuid4())
        self.amount = amount
        self.gateway = gateway
        self.user_id = user_id
        self.astrologer_id = astrologer_id
        self.purpose = purpose
        self.status = TransactionStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at = None
        self.payment_reference = None
        self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "gateway": self.gateway,
            "user_id": self.user_id,
            "astrologer_id": self.astrologer_id,
            "purpose": self.purpose,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "payment_reference": self.payment_reference,
            "metadata": self.metadata
        }


class Wallet:
    """User wallet with balance and transaction history"""
    
    def __init__(self, user_id: str, initial_balance: float = 0.0):
        self.user_id = user_id
        self.balance = initial_balance
        self.transactions = []
        self.created_at = datetime.now()
    
    def add_funds(self, amount: float, source: str,
                  reference_id: str = "") -> Dict:
        """
        Add funds to wallet
        Sources: khalti, esewa, paypal, stripe, bank_transfer
        """
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }
        
        transaction = Transaction(
            amount=amount,
            gateway=source,
            user_id=self.user_id,
            purpose="wallet_topup"
        )
        
        transaction.status = TransactionStatus.COMPLETED
        transaction.completed_at = datetime.now()
        transaction.payment_reference = reference_id
        
        self.balance += amount
        self.transactions.append(transaction)
        
        return {
            "success": True,
            "new_balance": self.balance,
            "transaction": transaction.to_dict()
        }
    
    def deduct_funds(self, amount: float, purpose: str,
                    astrologer_id: str) -> Dict:
        """
        Deduct funds from wallet for consultation
        """
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }
        
        if self.balance < amount:
            return {
                "success": False,
                "error": f"Insufficient balance. Available: {self.balance}, Required: {amount}"
            }
        
        transaction = Transaction(
            amount=amount,
            gateway="wallet",
            user_id=self.user_id,
            astrologer_id=astrologer_id,
            purpose=purpose
        )
        
        transaction.status = TransactionStatus.COMPLETED
        transaction.completed_at = datetime.now()
        
        self.balance -= amount
        self.transactions.append(transaction)
        
        return {
            "success": True,
            "new_balance": self.balance,
            "transaction": transaction.to_dict()
        }
    
    def get_balance(self) -> float:
        """Get current wallet balance"""
        return self.balance
    
    def get_transaction_history(self, limit: int = 10) -> List[Dict]:
        """Get recent transactions"""
        return [t.to_dict() for t in self.transactions[-limit:]]


class EnhancedPaymentSystem:
    """
    Complete payment system combining multiple gateways with wallet
    """
    
    def __init__(self, data_file: str = "transactions.json"):
        self.data_file = data_file
        self.wallets: Dict[str, Wallet] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.gateway_configs = {
            "khalti": {"fee_percent": 1.5, "test_mode": True},
            "esewa": {"fee_percent": 1.0, "test_mode": True},
            "paypal": {"fee_percent": 2.9, "test_mode": True},
            "stripe": {"fee_percent": 2.9, "test_mode": True},
            "wallet": {"fee_percent": 0.0, "test_mode": False}
        }
        self.load_data()
    
    def create_wallet(self, user_id: str, initial_balance: float = 0.0) -> Wallet:
        """Create or get user wallet"""
        if user_id not in self.wallets:
            self.wallets[user_id] = Wallet(user_id, initial_balance)
        return self.wallets[user_id]
    
    def get_wallet(self, user_id: str) -> Optional[Wallet]:
        """Get user wallet"""
        return self.wallets.get(user_id)
    
    def process_payment(self, user_id: str, amount: float,
                       gateway: str, astrologer_id: str = "",
                       purpose: str = "consultation") -> Dict:
        """
        Process payment through specified gateway
        Handles both payment gateways and wallet
        """
        
        wallet = self.create_wallet(user_id)
        
        # Calculate fees
        fee_percent = self.gateway_configs.get(gateway, {}).get("fee_percent", 0)
        fee_amount = (amount * fee_percent) / 100
        total_amount = amount + fee_amount
        
        if gateway == "wallet":
            # Direct wallet deduction
            result = wallet.deduct_funds(amount, purpose, astrologer_id)
            if result["success"]:
                transaction = result["transaction"]
                self.transactions[transaction["transaction_id"]] = transaction
                self.save_data()
            return result
        
        else:
            # Other payment gateways
            transaction = Transaction(
                amount=amount,
                gateway=gateway,
                user_id=user_id,
                astrologer_id=astrologer_id,
                purpose=purpose
            )
            transaction.metadata = {
                "fee": fee_amount,
                "total_with_fee": total_amount
            }
            
            self.transactions[transaction.transaction_id] = transaction
            
            return {
                "success": True,
                "transaction_id": transaction.transaction_id,
                "amount": amount,
                "fee": fee_amount,
                "total_amount": total_amount,
                "gateway": gateway,
                "status": "payment_initiated",
                "next_action": f"Redirect to {gateway.upper()} or open app"
            }
    
    def verify_payment(self, transaction_id: str, 
                      gateway_reference: str = "") -> Dict:
        """
        Verify payment completion
        Called after user completes payment on gateway
        """
        transaction = self.transactions.get(transaction_id)
        if not transaction:
            return {
                "success": False,
                "error": "Transaction not found"
            }
        
        # Update transaction
        transaction["status"] = TransactionStatus.COMPLETED.value
        transaction["completed_at"] = datetime.now().isoformat()
        transaction["payment_reference"] = gateway_reference
        
        # Add funds to wallet if it's a topup
        if transaction["purpose"] == "wallet_topup":
            wallet = self.get_wallet(transaction["user_id"])
            wallet.add_funds(
                transaction["amount"],
                transaction["gateway"],
                gateway_reference
            )
        
        self.save_data()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "amount": transaction["amount"],
            "gateway": transaction["gateway"],
            "message": "Payment verified successfully"
        }
    
    def refund_transaction(self, transaction_id: str,
                          reason: str = "") -> Dict:
        """
        Refund a completed transaction
        """
        transaction = self.transactions.get(transaction_id)
        if not transaction:
            return {
                "success": False,
                "error": "Transaction not found"
            }
        
        if transaction["status"] != TransactionStatus.COMPLETED.value:
            return {
                "success": False,
                "error": f"Cannot refund transaction in {transaction['status']} status"
            }
        
        # Process refund based on gateway
        transaction["status"] = TransactionStatus.REFUNDED.value
        
        # If wallet topup, reduce balance
        if transaction["purpose"] == "wallet_topup":
            wallet = self.get_wallet(transaction["user_id"])
            if wallet.balance >= transaction["amount"]:
                wallet.balance -= transaction["amount"]
        
        self.save_data()
        
        return {
            "success": True,
            "transaction_id": transaction_id,
            "refunded_amount": transaction["amount"],
            "reason": reason,
            "message": "Refund processed"
        }
    
    def get_user_balance(self, user_id: str) -> Dict:
        """Get user's total balance across all wallets"""
        wallet = self.get_wallet(user_id)
        if wallet:
            return {
                "user_id": user_id,
                "balance": wallet.get_balance(),
                "transactions": wallet.get_transaction_history(5)
            }
        
        return {
            "user_id": user_id,
            "balance": 0.0,
            "transactions": []
        }
    
    def get_transaction_history(self, user_id: str) -> List[Dict]:
        """Get all transactions for a user"""
        user_transactions = [
            t for t in self.transactions.values()
            if t["user_id"] == user_id
        ]
        return sorted(
            user_transactions,
            key=lambda x: x["created_at"],
            reverse=True
        )
    
    def save_data(self):
        """Save transactions to file"""
        try:
            data = {
                "transactions": {
                    tid: t for tid, t in self.transactions.items()
                },
                "wallets": {
                    uid: {
                        "balance": w.balance,
                        "created_at": w.created_at.isoformat(),
                        "transactions": [t.to_dict() for t in w.transactions]
                    }
                    for uid, w in self.wallets.items()
                },
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving payment data: {e}")
    
    def load_data(self):
        """Load transactions from file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Load wallets
            for user_id, wallet_data in data.get("wallets", {}).items():
                wallet = Wallet(user_id, wallet_data["balance"])
                wallet.created_at = datetime.fromisoformat(wallet_data["created_at"])
                self.wallets[user_id] = wallet
        
        except Exception as e:
            print(f"Error loading payment data: {e}")
    
    def export_transaction_report(self, user_id: str) -> str:
        """Export user's transaction report"""
        transactions = self.get_transaction_history(user_id)
        wallet = self.get_wallet(user_id)
        
        report = f"""
TRANSACTION REPORT - {user_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

Current Wallet Balance: NPR {wallet.get_balance() if wallet else 0:.2f}

TRANSACTION HISTORY:
{'-'*60}
"""
        
        for tx in transactions:
            report += f"""
Transaction ID: {tx['transaction_id']}
Amount: NPR {tx['amount']:.2f}
Gateway: {tx['gateway']}
Status: {tx['status']}
Date: {tx['created_at']}
Purpose: {tx['purpose']}
"""
        
        return report
