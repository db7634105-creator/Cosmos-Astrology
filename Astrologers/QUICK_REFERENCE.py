"""
QUICK REFERENCE - Country-Specific Payment System
==================================================

This file contains quick copy-paste code snippets for common operations.
"""

# ============================================================================
# 1. BASIC SETUP
# ============================================================================

from country_payment_gateway import (
    CountryPaymentGateway, CountryPaymentMapper,
    Country, PaymentProvider, KhaltiGateway, EsewaGateway, RazorpayGateway
)
from payment_system import PaymentSystem, PaymentMethod, PaymentStatus
from user_manager import UserManager


# ============================================================================
# 2. USER REGISTRATION WITH COUNTRY
# ============================================================================

def register_with_country():
    user_mgr = UserManager()
    
    # Nepal user
    success, msg = user_mgr.register_user(
        username="nepal_user",
        email="user@nepal.com",
        phone="+977-9800000000",
        password="pass123",
        region="nepal"
    )
    
    # India user
    success, msg = user_mgr.register_user(
        username="india_user",
        email="user@india.com",
        phone="+91-9876543210",
        password="pass123",
        region="india"
    )
    
    # Get user region
    region = user_mgr.get_user_region("nepal_user")  # Returns "nepal"
    
    # Update user region
    user_mgr.update_user_region("nepal_user", "india")


# ============================================================================
# 3. GET AVAILABLE PAYMENT METHODS FOR USER
# ============================================================================

def get_payment_methods():
    payment_sys = PaymentSystem()
    user_mgr = UserManager()
    
    username = "nepal_user"
    user_region = user_mgr.get_user_region(username)
    
    # Get all available providers for this region
    providers = payment_sys.get_available_payment_providers(user_region)
    # Output:
    # {
    #     "country": "nepal",
    #     "providers": [
    #         {"name": "khalti", "details": {...}},
    #         {"name": "esewa", "details": {...}}
    #     ]
    # }
    
    # Get default (primary) provider
    default = payment_sys.get_default_payment_provider(user_region)
    # Output: {"provider": "khalti", "details": {...}}


# ============================================================================
# 4. CREATE AND PROCESS PAYMENT - KHALTI (NEPAL)
# ============================================================================

def process_khalti_payment():
    payment_sys = PaymentSystem()
    
    # Create transaction
    transaction = payment_sys.create_transaction(
        customer_name="nepal_user",
        astrologer_name="Dr. Sharma",
        amount=500,
        payment_method=PaymentMethod.UPI,
        call_duration=15,
        country="nepal",
        payment_provider="khalti"
    )
    
    # Process payment
    success, message = payment_sys.process_payment(
        transaction,
        phone_number="+977-9800000000"
    )
    
    if success:
        print(f"✓ Payment successful! {message}")
    else:
        print(f"✗ Payment failed! {message}")


# ============================================================================
# 5. CREATE AND PROCESS PAYMENT - ESEWA (NEPAL)
# ============================================================================

def process_esewa_payment():
    payment_sys = PaymentSystem()
    
    # Create transaction
    transaction = payment_sys.create_transaction(
        customer_name="nepal_user",
        astrologer_name="Dr. Sharma",
        amount=500,
        payment_method=PaymentMethod.UPI,
        call_duration=15,
        country="nepal",
        payment_provider="esewa"
    )
    
    # Process payment
    success, message = payment_sys.process_payment(
        transaction,
        email="user@esewa.com.np"
    )
    
    if success:
        print(f"✓ Payment successful! {message}")
    else:
        print(f"✗ Payment failed! {message}")


# ============================================================================
# 6. CREATE AND PROCESS PAYMENT - RAZORPAY UPI (INDIA)
# ============================================================================

def process_razorpay_upi_payment():
    payment_sys = PaymentSystem()
    
    # Create transaction
    transaction = payment_sys.create_transaction(
        customer_name="india_user",
        astrologer_name="Dr. Sharma",
        amount=500,
        payment_method=PaymentMethod.UPI,
        call_duration=15,
        country="india",
        payment_provider="razorpay"
    )
    
    # Process payment
    success, message = payment_sys.process_payment(
        transaction,
        upi_id="user@okhdfcbank"
    )
    
    if success:
        print(f"✓ Payment successful! {message}")
    else:
        print(f"✗ Payment failed! {message}")


# ============================================================================
# 7. CREATE AND PROCESS PAYMENT - RAZORPAY PHONE (INDIA)
# ============================================================================

def process_razorpay_phone_payment():
    payment_sys = PaymentSystem()
    
    # Create transaction
    transaction = payment_sys.create_transaction(
        customer_name="india_user",
        astrologer_name="Dr. Sharma",
        amount=500,
        payment_method=PaymentMethod.UPI,
        call_duration=15,
        country="india",
        payment_provider="razorpay"
    )
    
    # Process payment
    success, message = payment_sys.process_payment(
        transaction,
        phone_number="+91-9876543210"
    )
    
    if success:
        print(f"✓ Payment successful! {message}")
    else:
        print(f"✗ Payment failed! {message}")


# ============================================================================
# 8. VALIDATE PHONE NUMBERS
# ============================================================================

def validate_phone_numbers():
    # Khalti (Nepal) - starts with 98 or 97
    print(KhaltiGateway.validate_phone("+977-9800000000"))  # True
    print(KhaltiGateway.validate_phone("9800000000"))       # True
    print(KhaltiGateway.validate_phone("+977-9600000000"))  # False
    
    # Razorpay (India) - starts with 6-9
    print(RazorpayGateway.validate_phone("+91-9876543210")) # True
    print(RazorpayGateway.validate_phone("9876543210"))     # True
    print(RazorpayGateway.validate_phone("+91-5876543210")) # False


# ============================================================================
# 9. VALIDATE UPI IDS
# ============================================================================

def validate_upi_ids():
    # Razorpay UPI format
    print(RazorpayGateway.validate_upi("user@okhdfcbank"))  # True
    print(RazorpayGateway.validate_upi("john@icici"))       # True
    print(RazorpayGateway.validate_upi("invalid"))          # False


# ============================================================================
# 10. VALIDATE EMAILS
# ============================================================================

def validate_emails():
    # Esewa email format
    print(EsewaGateway.validate_email("user@esewa.com.np")) # True
    print(EsewaGateway.validate_email("john@gmail.com"))    # True
    print(EsewaGateway.validate_email("invalid"))           # False


# ============================================================================
# 11. GET PAYMENT INSTRUCTIONS
# ============================================================================

def get_payment_instructions():
    from country_payment_gateway import PaymentProvider
    
    # Get instructions for each provider
    instructions = CountryPaymentGateway.get_payment_instructions(None, PaymentProvider.KHALTI)
    print(f"Name: {instructions['name']}")
    print(f"Country: {instructions['country']}")
    print(f"Description: {instructions['description']}")
    print(f"Methods: {instructions['supported_methods']}")
    print(f"Instruction: {instructions['instruction']}")


# ============================================================================
# 12. DIRECT GATEWAY PROCESSING (LOW LEVEL)
# ============================================================================

def direct_gateway_processing():
    # Process payment directly via specific gateway
    
    # Khalti
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.KHALTI,
        amount=500,
        transaction_id="TXN_001",
        phone_number="+977-9800000000"
    )
    
    # Esewa
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.ESEWA,
        amount=500,
        transaction_id="TXN_002",
        email="user@esewa.com.np"
    )
    
    # Razorpay UPI
    success, msg = CountryPaymentGateway.process_payment(
        Country.INDIA,
        PaymentProvider.RAZORPAY,
        amount=500,
        transaction_id="TXN_003",
        upi_id="user@bank",
        payment_method="upi"
    )
    
    # Razorpay Phone
    success, msg = CountryPaymentGateway.process_payment(
        Country.INDIA,
        PaymentProvider.RAZORPAY,
        amount=500,
        transaction_id="TXN_004",
        phone_number="+91-9876543210",
        payment_method="phone"
    )


# ============================================================================
# 13. COUNTRY MAPPING
# ============================================================================

def country_mapping_operations():
    # Convert string region to Country enum
    country = CountryPaymentMapper.get_country_from_region("nepal")
    # Returns: Country.NEPAL
    
    # Get available providers for country
    providers = CountryPaymentMapper.get_available_providers(country)
    # Returns: [PaymentProvider.KHALTI, PaymentProvider.ESEWA]
    
    # Get default provider
    default = CountryPaymentMapper.get_default_provider(country)
    # Returns: PaymentProvider.KHALTI
    
    # Works with string too
    providers = CountryPaymentMapper.get_available_providers(
        CountryPaymentMapper.get_country_from_region("india")
    )
    # Returns: [PaymentProvider.RAZORPAY]


# ============================================================================
# 14. TRANSACTION HISTORY BY PROVIDER
# ============================================================================

def get_transaction_history():
    payment_sys = PaymentSystem()
    
    # Get all transactions
    all_txns = payment_sys.get_transaction_history()
    
    # Filter by country (manual)
    nepal_txns = [t for t in all_txns if t.get('country') == 'nepal']
    
    # Filter by provider (manual)
    khalti_txns = [t for t in all_txns if t.get('payment_provider') == 'khalti']
    
    # Get customer history
    customer_txns = payment_sys.get_transaction_history("nepal_user")


# ============================================================================
# 15. COMMON PAYMENT AMOUNTS
# ============================================================================

PAYMENT_AMOUNTS = {
    "5_min": 99,      # ₹99 or ₨99
    "15_min": 249,    # ₹249 or ₨249
    "30_min": 449,    # ₹449 or ₨449
    "60_min": 799,    # ₹799 or ₨799
}


# ============================================================================
# 16. FULL PAYMENT FLOW EXAMPLE
# ============================================================================

def complete_payment_flow():
    """
    Complete example of payment flow from registration to payment
    """
    
    # Step 1: Register user
    user_mgr = UserManager()
    user_mgr.register_user(
        username="astro_customer",
        email="customer@example.com",
        phone="+977-9800000000",
        password="secure123",
        region="nepal"
    )
    
    # Step 2: Get user's region and available payment methods
    user_region = user_mgr.get_user_region("astro_customer")
    payment_sys = PaymentSystem()
    available_methods = payment_sys.get_available_payment_providers(user_region)
    
    print(f"User Region: {user_region}")
    print(f"Available Providers: {[p['name'] for p in available_methods['providers']]}")
    
    # Step 3: Create transaction
    transaction = payment_sys.create_transaction(
        customer_name="astro_customer",
        astrologer_name="Dr. Sharma",
        amount=PAYMENT_AMOUNTS["15_min"],
        payment_method=PaymentMethod.UPI,
        call_duration=15,
        country=user_region,
        payment_provider="khalti"
    )
    
    # Step 4: Process payment
    success, message = payment_sys.process_payment(
        transaction,
        phone_number="+977-9800000000"
    )
    
    # Step 5: Check result
    if success:
        print(f"✓ {message}")
        print(f"Transaction ID: {transaction.transaction_id}")
        print(f"Status: {transaction.status.value}")
    else:
        print(f"✗ {message}")


# ============================================================================
# 17. ERROR HANDLING
# ============================================================================

def handle_payment_errors():
    """
    Examples of error handling
    """
    payment_sys = PaymentSystem()
    
    # Invalid phone for Khalti
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.KHALTI,
        500,
        "TXN_001",
        phone_number="invalid"
    )
    # Result: success=False, msg="Invalid Nepali phone number format (should start with 98/97)"
    
    # Missing email for Esewa
    success, msg = CountryPaymentGateway.process_payment(
        Country.NEPAL,
        PaymentProvider.ESEWA,
        500,
        "TXN_002",
        email=""
    )
    # Result: success=False, msg="Email required for Esewa"
    
    # Invalid amount
    success, msg = CountryPaymentGateway.process_payment(
        Country.INDIA,
        PaymentProvider.RAZORPAY,
        -100,
        "TXN_003",
        upi_id="user@bank"
    )
    # Result: success=False, msg="Invalid amount"


# ============================================================================
# 18. TESTING QUICK COMMANDS
# ============================================================================

"""
# Run tests
python test_country_payment.py

# Quick Python tests
python -c "
from country_payment_gateway import CountryPaymentMapper, Country
print(CountryPaymentMapper.get_available_providers(Country.NEPAL))
"

# Get available methods for Nepal
python -c "
from payment_system import PaymentSystem
ps = PaymentSystem()
print(ps.get_available_payment_providers('nepal'))
"

# Validate phone numbers
python -c "
from country_payment_gateway import KhaltiGateway, RazorpayGateway
print('Khalti:', KhaltiGateway.validate_phone('+977-9800000000'))
print('Razorpay:', RazorpayGateway.validate_phone('+91-9876543210'))
"
"""


# ============================================================================
# 19. DEBUGGING TIPS
# ============================================================================

"""
# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)

# Print transaction object
transaction = payment_sys.create_transaction(...)
print(transaction.to_dict())

# Check user info
user_info = user_mgr.get_user_info("username")
print(user_info)

# List all transactions
all_txns = payment_sys.get_transaction_history()
for txn in all_txns:
    print(f"{txn['transaction_id']}: {txn['country']} - {txn['payment_provider']}")
"""


# ============================================================================
# 20. COMMON PATTERNS
# ============================================================================

"""
PATTERN 1: Get payment providers for logged-in user
-----------------------------------------------------
user_region = user_mgr.get_user_region(current_user)
providers = payment_sys.get_available_payment_providers(user_region)
for provider in providers['providers']:
    print(provider['name'])


PATTERN 2: Process payment with automatic provider selection
-----------------------------------------------------
user_region = user_mgr.get_user_region(customer)
default_provider = payment_sys.get_default_payment_provider(user_region)
transaction = payment_sys.create_transaction(
    customer, astrologer, amount, PaymentMethod.UPI,
    country=user_region,
    payment_provider=default_provider['provider']
)
success, msg = payment_sys.process_payment(transaction, **payment_details)


PATTERN 3: Validate input for specific provider
-----------------------------------------------------
country = CountryPaymentMapper.get_country_from_region(user_region)
providers = CountryPaymentMapper.get_available_providers(country)

if PaymentProvider.KHALTI in providers:
    is_valid = KhaltiGateway.validate_phone(phone_input)
elif PaymentProvider.RAZORPAY in providers:
    is_valid = RazorpayGateway.validate_upi(upi_input)


PATTERN 4: Create payment UI dynamically
-----------------------------------------------------
user_region = user_mgr.get_user_region(current_user)
providers = payment_sys.get_available_payment_providers(user_region)

for provider in providers['providers']:
    instructions = CountryPaymentGateway.get_payment_instructions(
        CountryPaymentMapper.get_country_from_region(user_region),
        PaymentProvider[provider['name'].upper()]
    )
    display_ui_for_provider(instructions)
"""


if __name__ == "__main__":
    print("Quick Reference - Country-Specific Payment System")
    print("See code comments for copy-paste examples")
    print("\nRun test suite: python test_country_payment.py")
