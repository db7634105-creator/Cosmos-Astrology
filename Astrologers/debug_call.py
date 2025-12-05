#!/usr/bin/env python3
"""Debug script to identify errors when connecting free call"""

import sys
import traceback

sys.path.insert(0, r"c:\Users\asus\OneDrive\Desktop\KundaliAI\Cosmos-Astrology\Astrologers")

try:
    print("1. Testing imports...")
    from call_manager import CallManager
    from astrologers_data import ASTROLOGERS
    from payment_system import PaymentSystem, PaymentMethod
    print("   ✓ All imports successful")
    
    print("\n2. Testing PaymentSystem...")
    ps = PaymentSystem()
    print("   ✓ PaymentSystem initialized")
    
    print("\n3. Testing transaction creation...")
    user = "testuser"
    astrologer = ASTROLOGERS[0]['name']
    
    # Create transaction like the code does
    transaction = ps.create_transaction(
        user,
        astrologer,
        0,  # FREE
        PaymentMethod.WALLET,
        15  # duration
    )
    print(f"   ✓ Transaction created: {transaction.transaction_id}")
    print(f"   ✓ Transaction object type: {type(transaction)}")
    print(f"   ✓ Has 'to_dict' method: {hasattr(transaction, 'to_dict')}")
    
    print("\n4. Testing transaction.to_dict()...")
    txn_dict = transaction.to_dict()
    print(f"   ✓ to_dict() works: {type(txn_dict)}")
    print(f"   ✓ Keys: {txn_dict.keys()}")
    
    print("\n5. Testing save_transactions...")
    ps.transactions.append(txn_dict)
    ps.save_transactions()
    print("   ✓ Transactions saved")
    
    print("\n6. Testing CallManager...")
    cm = CallManager()
    call = cm.start_call("test-call", user, astrologer, "+977-123", 15)
    print(f"   ✓ Call started: {call['call_id']}")
    print(f"   ✓ Call is active: {cm.is_call_active('test-call')}")
    
    print("\n✅ ALL DIAGNOSTIC TESTS PASSED - System logic is OK")
    print("\nThe error is likely in the UI threading or window handling.")
    
except Exception as e:
    print(f"\n❌ ERROR FOUND:")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error message: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
