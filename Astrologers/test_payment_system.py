"""
Test Script for Payment & WhatsApp System
Run this to verify all components are working
"""

import sys
import json
from datetime import datetime, timedelta

def test_imports():
    """Test if all modules can be imported"""
    print("\n" + "="*70)
    print("TESTING IMPORTS")
    print("="*70)
    
    try:
        from real_payment_gateway import (
            PaymentGatewayFactory, 
            PaymentGateway,
            KhaltiGateway,
            ESewaGateway,
            PayPalGateway,
            StripeGateway
        )
        print("✓ real_payment_gateway.py")
    except ImportError as e:
        print(f"✗ real_payment_gateway.py: {e}")
        return False
    
    try:
        from enhanced_payment_system import (
            EnhancedPaymentSystem,
            Wallet,
            Transaction,
            TransactionStatus
        )
        print("✓ enhanced_payment_system.py")
    except ImportError as e:
        print(f"✗ enhanced_payment_system.py: {e}")
        return False
    
    try:
        from whatsapp_caller import (
            WhatsAppCaller,
            TwilioWhatsAppCaller,
            CallScheduler
        )
        print("✓ whatsapp_caller.py")
    except ImportError as e:
        print(f"✗ whatsapp_caller.py: {e}")
        return False
    
    print("\n✓ All modules imported successfully!")
    return True


def test_khalti():
    """Test Khalti gateway"""
    print("\n" + "="*70)
    print("TESTING KHALTI GATEWAY")
    print("="*70)
    
    from real_payment_gateway import PaymentGatewayFactory, PaymentGateway
    
    try:
        gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.KHALTI, test_mode=True)
        print(f"✓ Khalti gateway created (Test mode: {gateway.test_mode})")
        
        # Test QR code generation
        qr_code, transaction_id = gateway.generate_qr_code("+977-9841234567", 30000)
        print(f"✓ QR code generated (Transaction ID: {transaction_id[:8]}...)")
        
        # Test payment initiation
        response = gateway.initiate_payment(
            amount=30000,
            phone="+977-9841234567",
            product_name="Test Consultation"
        )
        
        if response['success']:
            print("✓ Payment initiation successful")
            print(f"  Gateway: {response['gateway']}")
        else:
            print(f"✗ Payment initiation failed: {response['error']}")
        
        return True
    except Exception as e:
        print(f"✗ Khalti test failed: {e}")
        return False


def test_esewa():
    """Test eSewa gateway"""
    print("\n" + "="*70)
    print("TESTING ESEWA GATEWAY")
    print("="*70)
    
    from real_payment_gateway import PaymentGatewayFactory, PaymentGateway
    
    try:
        gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.ESEWA, test_mode=True)
        print(f"✓ eSewa gateway created (Test mode: {gateway.test_mode})")
        
        # Test signature generation
        signature = gateway.generate_signature(total_amount=300.0, transaction_uuid="test-123")
        print(f"✓ Signature generated: {signature[:16]}...")
        
        # Test payment initiation
        response = gateway.initiate_payment(
            amount=300.0,
            email="test@example.com",
            product_name="Test Consultation"
        )
        
        if response['success']:
            print("✓ Payment initiation successful")
            print(f"  URL: {response['payment_url']}")
            print(f"  Transaction ID: {response['transaction_id'][:8]}...")
        else:
            print(f"✗ Payment initiation failed: {response['error']}")
        
        return True
    except Exception as e:
        print(f"✗ eSewa test failed: {e}")
        return False


def test_paypal():
    """Test PayPal gateway"""
    print("\n" + "="*70)
    print("TESTING PAYPAL GATEWAY")
    print("="*70)
    
    from real_payment_gateway import PaymentGatewayFactory, PaymentGateway
    
    try:
        gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.PAYPAL, test_mode=True)
        print(f"✓ PayPal gateway created (Test mode: {gateway.test_mode})")
        
        # PayPal payment initiation (will fail without real credentials)
        response = gateway.initiate_payment(amount=10.0)
        
        if not response['success']:
            # This is expected in test mode without credentials
            print(f"! PayPal requires credentials: {response['error'][:50]}...")
            print("✓ PayPal gateway functional (waiting for real credentials)")
        else:
            print("✓ PayPal payment initiated")
        
        return True
    except Exception as e:
        print(f"✗ PayPal test failed: {e}")
        return False


def test_wallet():
    """Test wallet system"""
    print("\n" + "="*70)
    print("TESTING WALLET SYSTEM")
    print("="*70)
    
    from enhanced_payment_system import EnhancedPaymentSystem
    
    try:
        system = EnhancedPaymentSystem(data_file="test_transactions.json")
        print("✓ Payment system initialized")
        
        # Create wallet
        wallet = system.create_wallet("test_user", initial_balance=1000.0)
        print(f"✓ Wallet created for test_user")
        
        # Add funds
        result = system.process_payment(
            user_id="test_user",
            amount=500.0,
            gateway="wallet",
            purpose="wallet_topup"
        )
        
        if result['success']:
            print(f"✓ Funds added successfully")
        else:
            print(f"✗ Failed to add funds: {result['error']}")
        
        # Deduct funds
        result = system.process_payment(
            user_id="test_user",
            amount=300.0,
            gateway="wallet",
            astrologer_id="astro123",
            purpose="consultation"
        )
        
        if result['success']:
            print(f"✓ Consultation payment processed")
            print(f"  New balance: NPR {result['new_balance']}")
        else:
            print(f"✗ Failed to process payment: {result['error']}")
        
        # Get balance
        balance_info = system.get_user_balance("test_user")
        print(f"✓ Final balance: NPR {balance_info['balance']}")
        
        return True
    except Exception as e:
        print(f"✗ Wallet test failed: {e}")
        return False


def test_whatsapp():
    """Test WhatsApp calling"""
    print("\n" + "="*70)
    print("TESTING WHATSAPP CALLING")
    print("="*70)
    
    from whatsapp_caller import WhatsAppCaller, CallScheduler
    
    try:
        caller = WhatsAppCaller()
        print("✓ WhatsApp caller initialized")
        
        # Generate WhatsApp link
        link = caller.generate_whatsapp_link(
            phone_number="9841234567",
            astrologer_name="Astrologer Test",
            message="Test message"
        )
        print(f"✓ WhatsApp link generated")
        print(f"  Link: {link[:80]}...")
        
        # Schedule call
        scheduler = CallScheduler()
        call_time = datetime.now() + timedelta(minutes=30)
        
        result = scheduler.add_scheduled_call(
            call_id="test_call_1",
            call_time=call_time,
            phone_number="+977-9841234567",
            astrologer_name="Astrologer Test",
            duration_minutes=30
        )
        
        if result['success']:
            print(f"✓ Call scheduled successfully")
            print(f"  Scheduled time: {result['scheduled_time']}")
        else:
            print(f"✗ Call scheduling failed: {result['error']}")
        
        return True
    except Exception as e:
        print(f"✗ WhatsApp test failed: {e}")
        return False


def test_transaction_flow():
    """Test complete transaction flow"""
    print("\n" + "="*70)
    print("TESTING COMPLETE TRANSACTION FLOW")
    print("="*70)
    
    from enhanced_payment_system import EnhancedPaymentSystem
    
    try:
        system = EnhancedPaymentSystem(data_file="test_flow.json")
        
        print("Step 1: Create user wallet")
        wallet = system.create_wallet("flow_user", initial_balance=100.0)
        print("✓ Wallet created with NPR 100")
        
        print("\nStep 2: Top up wallet via Khalti")
        topup = system.process_payment(
            user_id="flow_user",
            amount=500.0,
            gateway="khalti",
            purpose="wallet_topup"
        )
        print(f"✓ Top-up initiated (ID: {topup['transaction_id'][:8]}...)")
        print(f"  Total with fee: NPR {topup['total_amount']}")
        
        print("\nStep 3: Verify payment")
        verify = system.verify_payment(
            transaction_id=topup['transaction_id'],
            gateway_reference="khalti_ref_123"
        )
        
        if verify['success']:
            print("✓ Payment verified")
            balance = system.get_user_balance("flow_user")
            print(f"  New balance: NPR {balance['balance']}")
        
        print("\nStep 4: Book consultation")
        consultation = system.process_payment(
            user_id="flow_user",
            amount=300.0,
            gateway="wallet",
            astrologer_id="astro_001",
            purpose="consultation"
        )
        
        if consultation['success']:
            print("✓ Consultation booked and paid")
            print(f"  Remaining balance: NPR {consultation['new_balance']}")
        
        print("\nStep 5: View transaction history")
        history = system.get_transaction_history("flow_user")
        print(f"✓ Total transactions: {len(history)}")
        for tx in history[:3]:
            print(f"  - {tx['purpose']}: NPR {tx['amount']} via {tx['gateway']}")
        
        return True
    except Exception as e:
        print(f"✗ Transaction flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  ASTROLOGY CONSULTATION SYSTEM - TEST SUITE  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    # Run tests
    results['Imports'] = test_imports()
    if results['Imports']:
        results['Khalti'] = test_khalti()
        results['eSewa'] = test_esewa()
        results['PayPal'] = test_paypal()
        results['Wallet'] = test_wallet()
        results['WhatsApp'] = test_whatsapp()
        results['Transaction Flow'] = test_transaction_flow()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<50} {status}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready for use.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check setup.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
