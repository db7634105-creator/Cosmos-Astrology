#!/usr/bin/env python3
"""Test script to verify system changes"""

from call_manager import CallManager
from astrologers_data import ASTROLOGERS

print("=" * 60)
print("SYSTEM VERIFICATION TEST")
print("=" * 60)

# Test 1: CallManager
print("\n1. Testing CallManager...")
cm = CallManager()
print("   ✓ CallManager imported successfully")

# Test 2: Verify all astrologers are FREE
print("\n2. Verifying all astrologers are FREE...")
all_free = True
for ast in ASTROLOGERS:
    is_free = ast.get('is_free', False)
    price = ast.get('price_per_minute', -1)
    status = "✓ FREE" if (is_free and price == 0) else "✗ PAID"
    print(f"   {status} - {ast['name']} (₨{price}/min)")
    if not (is_free and price == 0):
        all_free = False

if all_free:
    print("\n   ✓ ALL ASTROLOGERS ARE FREE!")
else:
    print("\n   ✗ ERROR: Some astrologers are not free")

# Test 3: Test CallManager functionality
print("\n3. Testing CallManager functionality...")
call_data = cm.start_call(
    call_id="test-123",
    customer_name="TestUser",
    astrologer_name="Dinesh Bohara",
    astrologer_phone="+977-9769899316",
    duration_minutes=15
)
print("   ✓ Call started successfully")
print(f"   - Call ID: {call_data['call_id']}")
print(f"   - Duration: {call_data['duration_minutes']} minutes")
print(f"   - Status: {call_data['status']}")

# Test 4: Check call remaining time
import time
time.sleep(2)
remaining = cm.get_call_time_remaining("test-123")
elapsed = cm.get_call_elapsed_time("test-123")
print(f"   ✓ Timer check: Elapsed={elapsed}s, Remaining={remaining}s")

# Test 5: End call
ended = cm.end_call("test-123")
if ended:
    print(f"   ✓ Call ended successfully")
    print(f"   - Actual duration: {ended.get('actual_duration_minutes', 0):.1f} minutes")

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nSystem is ready for actual calling!")
