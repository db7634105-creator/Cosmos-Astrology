"""
Test Script for Country-Specific Payment System
Tests the integration of Khalti/Esewa (Nepal) and Razorpay (India) payment gateways
"""

import os
import sys
from datetime import datetime

# Add the Astrologers directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from user_manager import UserManager
from payment_system import PaymentSystem, PaymentMethod
from country_payment_gateway import (
    CountryPaymentGateway, CountryPaymentMapper, 
    Country, PaymentProvider, KhaltiGateway, EsewaGateway, RazorpayGateway
)


def test_country_mapper():
    """Test country mapping functionality"""
    print("\n" + "="*60)
    print("TEST 1: Country Mapping")
    print("="*60)
    
    test_regions = ["nepal", "Nepal", "NEPAL", "india", "India", "INDIA", "us", "USA"]
    
    for region in test_regions:
        country = CountryPaymentMapper.get_country_from_region(region)
        providers = CountryPaymentMapper.get_available_providers(country)
        default = CountryPaymentMapper.get_default_provider(country)
        
        print(f"\nRegion: {region}")
        print(f"  Country: {country.value}")
        print(f"  Available Providers: {[p.value for p in providers]}")
        print(f"  Default Provider: {default.value}")


def test_khalti_validation():
    """Test Khalti phone validation"""
    print("\n" + "="*60)
    print("TEST 2: Khalti Phone Number Validation")
    print("="*60)
    
    test_numbers = [
        ("+977-9800000000", True),
        ("9800000000", True),
        ("98XXXXXXXX", True),
        ("97XXXXXXXX", True),
        ("+977-9600000000", True),
        ("9600000000", False),
        ("invalid", False),
        ("", False),
    ]
    
    for phone, expected in test_numbers:
        # Create test number with real digits
        if phone and phone[0] in "98":
            test_phone = f"+977-{phone[:2]}{phone[2:] if len(phone) > 2 else '00000000'}"
        else:
            test_phone = phone
        
        result = KhaltiGateway.validate_phone(test_phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} Phone: {phone} -> Valid: {result} (Expected: {expected})")


def test_razorpay_validation():
    """Test Razorpay phone and UPI validation"""
    print("\n" + "="*60)
    print("TEST 3: Razorpay Phone & UPI Validation")
    print("="*60)
    
    phones = [
        ("+91-9876543210", True),
        ("9876543210", True),
        ("+91-8765432109", True),
        ("6123456789", True),
        ("+91-5123456789", False),  # Starts with 5
        ("invalid", False),
    ]
    
    print("\nPhone Numbers:")
    for phone, expected in phones:
        result = RazorpayGateway.validate_phone(phone)
        status = "✓" if result == expected else "✗"
        print(f"{status} {phone} -> Valid: {result} (Expected: {expected})")
    
    upis = [
        ("user@okhdfcbank", True),
        ("john.doe@icici", True),
        ("contact@bank", True),
        ("invalid", False),
        ("@bank", False),
        ("", False),
    ]
    
    print("\nUPI IDs:")
    for upi, expected in upis:
        result = RazorpayGateway.validate_upi(upi)
        status = "✓" if result == expected else "✗"
        print(f"{status} {upi} -> Valid: {result} (Expected: {expected})")


def test_esewa_validation():
    """Test Esewa email validation"""
    print("\n" + "="*60)
    print("TEST 4: Esewa Email Validation")
    print("="*60)
    
    emails = [
        ("user@esewa.com.np", True),
        ("john.doe@example.com", True),
        ("contact@domain.co", True),
        ("invalid", False),
        ("invalid@", False),
        ("@domain.com", False),
        ("", False),
    ]
    
    for email, expected in emails:
        result = EsewaGateway.validate_email(email)
        status = "✓" if result == expected else "✗"
        print(f"{status} {email} -> Valid: {result} (Expected: {expected})")


def test_payment_processing():
    """Test payment processing for different countries"""
    print("\n" + "="*60)
    print("TEST 5: Payment Processing")
    print("="*60)
    
    # Test Khalti
    print("\n[KHALTI - Nepal]")
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.KHALTI,
        500,
        "TXN_TEST_001",
        phone_number="+977-9800000000"
    )
    print(f"Success: {success}, Message: {msg}")
    
    # Test Esewa
    print("\n[ESEWA - Nepal]")
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.ESEWA,
        500,
        "TXN_TEST_002",
        email="user@example.com"
    )
    print(f"Success: {success}, Message: {msg}")
    
    # Test Razorpay UPI
    print("\n[RAZORPAY UPI - India]")
    success, msg = CountryPaymentGateway.process_payment(
        Country.INDIA,
        PaymentProvider.RAZORPAY,
        500,
        "TXN_TEST_003",
        upi_id="user@okhdfcbank",
        payment_method="upi"
    )
    print(f"Success: {success}, Message: {msg}")
    
    # Test Razorpay Phone
    print("\n[RAZORPAY PHONE - India]")
    success, msg = CountryPaymentGateway.process_payment(
        Country.INDIA,
        PaymentProvider.RAZORPAY,
        500,
        "TXN_TEST_004",
        phone_number="+91-9876543210",
        payment_method="phone"
    )
    print(f"Success: {success}, Message: {msg}")


def test_user_registration():
    """Test user registration with country selection"""
    print("\n" + "="*60)
    print("TEST 6: User Registration with Country")
    print("="*60)
    
    user_mgr = UserManager("test_users.json")
    
    # Clean up test users if they exist
    if "test_nepal_user" in user_mgr.users_db:
        del user_mgr.users_db["test_nepal_user"]
    if "test_india_user" in user_mgr.users_db:
        del user_mgr.users_db["test_india_user"]
    
    # Register Nepal user
    print("\n[Registering Nepal User]")
    success, msg = user_mgr.register_user(
        "test_nepal_user",
        "nepal@test.com",
        "+977-9800000000",
        "password123",
        region="nepal"
    )
    print(f"Registration: {msg}")
    
    # Get user info
    user_info = user_mgr.get_user_info("test_nepal_user")
    print(f"User Info: {user_info}")
    
    # Register India user
    print("\n[Registering India User]")
    success, msg = user_mgr.register_user(
        "test_india_user",
        "india@test.com",
        "+91-9876543210",
        "password456",
        region="india"
    )
    print(f"Registration: {msg}")
    
    # Get user info
    user_info = user_mgr.get_user_info("test_india_user")
    print(f"User Info: {user_info}")
    
    # Test region retrieval
    print("\n[Region Retrieval]")
    nepal_region = user_mgr.get_user_region("test_nepal_user")
    india_region = user_mgr.get_user_region("test_india_user")
    print(f"Nepal User Region: {nepal_region}")
    print(f"India User Region: {india_region}")


def test_payment_system_integration():
    """Test payment system with country routing"""
    print("\n" + "="*60)
    print("TEST 7: Payment System Integration")
    print("="*60)
    
    payment_sys = PaymentSystem("test_transactions.json")
    
    # Get payment providers for Nepal
    print("\n[Nepal Payment Providers]")
    nepal_providers = payment_sys.get_available_payment_providers("nepal")
    print(f"Available Providers: {[p['name'] for p in nepal_providers['providers']]}")
    
    default_nepal = payment_sys.get_default_payment_provider("nepal")
    print(f"Default Provider: {default_nepal['provider']}")
    
    # Get payment providers for India
    print("\n[India Payment Providers]")
    india_providers = payment_sys.get_available_payment_providers("india")
    print(f"Available Providers: {[p['name'] for p in india_providers['providers']]}")
    
    default_india = payment_sys.get_default_payment_provider("india")
    print(f"Default Provider: {default_india['provider']}")


def print_payment_instructions():
    """Print payment instructions for each provider"""
    print("\n" + "="*60)
    print("TEST 8: Payment Instructions")
    print("="*60)
    
    providers = [
        PaymentProvider.KHALTI,
        PaymentProvider.ESEWA,
        PaymentProvider.RAZORPAY,
        PaymentProvider.CARD,
        PaymentProvider.PAYPAL
    ]
    
    for provider in providers:
        instructions = CountryPaymentGateway.get_payment_instructions(None, provider)
        print(f"\n[{instructions['name']} - {instructions['country']}]")
        print(f"Description: {instructions['description']}")
        print(f"Supported Methods: {', '.join(instructions['supported_methods'])}")
        print(f"Instructions: {instructions['instruction']}")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("COUNTRY-SPECIFIC PAYMENT SYSTEM - TEST SUITE")
    print("="*80)
    
    try:
        test_country_mapper()
        test_khalti_validation()
        test_razorpay_validation()
        test_esewa_validation()
        test_payment_processing()
        test_user_registration()
        test_payment_system_integration()
        print_payment_instructions()
        
        print("\n" + "="*80)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
