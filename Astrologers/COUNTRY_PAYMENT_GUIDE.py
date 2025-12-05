"""
Country-Specific Payment Integration - Implementation Guide
===========================================================

Overview:
---------
This system automatically routes payments to the appropriate payment gateway
based on the user's registered country/region:

NEPAL:
  - Khalti (digital wallet)
  - Esewa (digital payment)

INDIA:
  - Razorpay (multi-method payment platform)

OTHERS:
  - Credit/Debit Card
  - PayPal

Key Components:
---------------

1. country_payment_gateway.py (NEW)
   - Defines payment providers and country mapping
   - Khalti/Esewa/Razorpay gateway implementations
   - Country-to-provider routing logic
   - Payment instruction generation

2. user_manager.py (UPDATED)
   - register_user() now accepts 'region' parameter
   - New methods:
     * get_user_region() - Get user's country
     * update_user_region() - Update user's country

3. payment_system.py (UPDATED)
   - Transaction class now tracks country and payment_provider
   - process_payment() now handles country-specific routing
   - New methods:
     * get_available_payment_providers(country) - List all providers for a country
     * get_default_payment_provider(country) - Get the primary provider

Integration Steps:
------------------

A. User Registration (in your GUI):

   from user_manager import UserManager
   
   user_manager = UserManager()
   success, msg = user_manager.register_user(
       username="john",
       email="john@example.com",
       phone="+977-9800000000",
       password="password123",
       region="nepal"  # NEW: Specify user's country
   )

B. Creating Payments:

   from payment_system import PaymentSystem, PaymentMethod, PaymentStatus
   
   payment_system = PaymentSystem()
   user_region = user_manager.get_user_region("john")  # "nepal"
   
   transaction = payment_system.create_transaction(
       customer_name="john",
       astrologer_name="Dr. Sharma",
       amount=499,
       payment_method=PaymentMethod.WALLET,
       country=user_region,  # NEW: Pass user's country
       payment_provider="khalti"  # NEW: Specify provider
   )

C. Processing Payments:

   # For Nepal - Khalti
   success, msg = payment_system.process_payment(
       transaction,
       phone_number="+977-9800000000"  # Required for Khalti
   )
   
   # For Nepal - Esewa
   success, msg = payment_system.process_payment(
       transaction,
       email="user@esewa.com.np"  # Required for Esewa
   )
   
   # For India - Razorpay (UPI)
   success, msg = payment_system.process_payment(
       transaction,
       upi_id="user@bank"  # Required for Razorpay UPI
   )
   
   # For India - Razorpay (Phone)
   success, msg = payment_system.process_payment(
       transaction,
       phone_number="+91-9876543210"  # Required for Razorpay Phone
   )

D. Getting Available Payment Methods for a User:

   providers = payment_system.get_available_payment_providers("nepal")
   # Output:
   # {
   #     "country": "nepal",
   #     "providers": [
   #         {
   #             "name": "khalti",
   #             "details": {
   #                 "name": "Khalti",
   #                 "country": "Nepal",
   #                 "description": "...",
   #                 "supported_methods": ["Phone Number"],
   #                 "instruction": "Enter your registered Khalti phone number"
   #             }
   #         },
   #         {
   #             "name": "esewa",
   #             "details": { ... }
   #         }
   #     ]
   # }

   default = payment_system.get_default_payment_provider("nepal")
   # Output: { "provider": "khalti", "details": { ... } }

Phone Number Validation:
------------------------
- Nepal: +977XXXXXXXXXX (10 digits after country code), or 98/97XXXXXXXX
- India: +91XXXXXXXXXX (10 digits after country code), or [6-9]XXXXXXXXX

UPI ID Validation (India):
- Format: username@bank
- Example: john@okhdfcbank, contact@icici

Email Validation (Esewa):
- Standard email format
- Example: user@example.com

GUI Integration Tips:
---------------------

1. In registration form:
   - Add a dropdown/combobox for region selection
   - Options: "Nepal", "India", "Other"

2. In payment dialog:
   - Query available_payment_providers() for the logged-in user
   - Display dynamic UI based on selected provider
   - For Khalti: Show phone input field
   - For Esewa: Show email input field
   - For Razorpay: Show UPI/Phone/Card input options

3. Status messages:
   - Show provider name in transaction confirmation
   - Example: "Payment successful via Khalti!"

File Changes Summary:
---------------------
- NEW: country_payment_gateway.py (370+ lines)
- MODIFIED: user_manager.py (added region tracking)
- MODIFIED: payment_system.py (added country routing)
- TO MODIFY: main.py (UI for payment provider selection)

Testing the Integration:
------------------------

# Test Nepal - Khalti
python -c "
from payment_system import PaymentSystem
ps = PaymentSystem()
providers = ps.get_available_payment_providers('nepal')
print(providers)
"

# Test India - Razorpay
python -c "
from payment_system import PaymentSystem
ps = PaymentSystem()
providers = ps.get_available_payment_providers('india')
print(providers)
"

Currency Considerations:
------------------------
- Nepal: NRS (Nepali Rupees) - Symbol: ₨
- India: INR (Indian Rupees) - Symbol: ₹
- Consider storing currency code in transaction for future multi-currency support

Future Enhancements:
--------------------
1. Add currency conversion based on country
2. Add actual API integration with Khalti, Esewa, Razorpay
3. Add transaction history filtering by payment provider
4. Add refund handling per payment provider
5. Add webhook support for payment confirmations
6. Add tax calculation per country
7. Add compliance reporting for each country

"""
