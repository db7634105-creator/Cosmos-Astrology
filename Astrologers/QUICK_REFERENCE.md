# Quick Reference Guide - Payment & WhatsApp Integration

## Installation (2 minutes)

```bash
cd c:\Users\dines\OneDrive\Desktop\Kundali\Astrologers
pip install -r requirements.txt
```

## Environment Setup (.env file)

Create file: `.env`

```env
# Khalti Test Credentials (Nepal)
KHALTI_PUBLIC_KEY=test_public_key_dc74e0fd57cb46cd93832722d9d48521
KHALTI_SECRET_KEY=test_secret_key_dc74e0fd57cb46cd93832722d9d48521

# eSewa Test Credentials (Nepal)
ESEWA_MERCHANT_CODE=EPAYTEST
ESEWA_MERCHANT_KEY=8gBm/:&EnhH.1/q

# PayPal Sandbox Credentials
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret

# Stripe Test Credentials
STRIPE_API_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key

# Twilio (Optional for automated WhatsApp)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=+1234567890
```

## Basic Usage Examples

### 1. Process Payment via Khalti

```python
from real_payment_gateway import PaymentGatewayFactory, PaymentGateway

# Create gateway instance
gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.KHALTI)

# Initiate payment (amount in paisa: 300 NPR = 30000 paisa)
response = gateway.initiate_payment(
    amount=30000,
    phone="+977XXXXXXXXXX",
    product_name="30-min Astrology Consultation"
)

if response['success']:
    qr_code, transaction_id = gateway.generate_qr_code(
        phone_number="+977XXXXXXXXXX",
        amount=30000
    )
    # Display QR code to user
    # User scans with phone
    # After payment, verify:
    verify = gateway.verify_payment(token=response_token, amount=30000)
```

### 2. Process Payment via eSewa

```python
from real_payment_gateway import PaymentGatewayFactory, PaymentGateway

gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.ESEWA)

# Prepare payment form
payment = gateway.initiate_payment(
    amount=300.0,  # NPR amount
    email="user@example.com",
    product_name="Astrology Consultation"
)

if payment['success']:
    # Redirect to: payment['payment_url']
    # With form_data: payment['form_data']
    
    # After user returns, verify:
    verify = gateway.verify_payment(
        transaction_id=payment['transaction_id'],
        status="Complete",
        ref_id=reference_id_from_callback
    )
```

### 3. Process Payment via PayPal

```python
from real_payment_gateway import PaymentGatewayFactory, PaymentGateway

gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.PAYPAL)

# Create payment
payment = gateway.initiate_payment(
    amount=10.0,  # USD or configured currency
    description="Astrology Consultation"
)

if payment['success']:
    # Redirect to: payment['approval_url']
    # User approves on PayPal
    # Gets returned with PaymentID and PayerID
    
    # Verify payment
    verify = gateway.verify_payment(
        payment_id=payment['payment_id'],
        payer_id=returned_payer_id
    )
```

### 4. Create User Wallet

```python
from enhanced_payment_system import EnhancedPaymentSystem

system = EnhancedPaymentSystem()

# Create wallet for user
wallet = system.create_wallet(user_id="user123", initial_balance=0.0)

# Check balance
balance = system.get_user_balance(user_id="user123")
print(f"Balance: NPR {balance['balance']}")

# View transaction history
history = system.get_transaction_history(user_id="user123")
for tx in history:
    print(f"{tx['transaction_id']}: NPR {tx['amount']} via {tx['gateway']}")
```

### 5. Top-up Wallet with Khalti

```python
from enhanced_payment_system import EnhancedPaymentSystem
from real_payment_gateway import PaymentGatewayFactory, PaymentGateway

system = EnhancedPaymentSystem()

# Process wallet topup
result = system.process_payment(
    user_id="user123",
    amount=500.0,  # NPR 500
    gateway="khalti",
    purpose="wallet_topup"
)

transaction_id = result['transaction_id']
print(f"Total with fee: NPR {result['total_amount']}")

# After user completes Khalti payment:
verify = system.verify_payment(
    transaction_id=transaction_id,
    gateway_reference=khalti_reference_id
)

# Wallet now has NPR 500
```

### 6. Pay for Consultation from Wallet

```python
from enhanced_payment_system import EnhancedPaymentSystem

system = EnhancedPaymentSystem()

# Deduct from wallet
result = system.process_payment(
    user_id="user123",
    amount=300.0,  # NPR 300 for consultation
    gateway="wallet",
    astrologer_id="astro456",
    purpose="consultation"
)

if result['success']:
    new_balance = result['new_balance']
    print(f"Payment processed. New balance: NPR {new_balance}")
else:
    print(f"Payment failed: {result['error']}")
```

### 7. Initiate WhatsApp Call

```python
from whatsapp_caller import WhatsAppCaller

caller = WhatsAppCaller()

# Start immediate call
result = caller.initiate_whatsapp_call(
    phone_number="+977XXXXXXXXXX",  # Astrologer's WhatsApp number
    astrologer_name="Astrologer Name",
    duration_minutes=30,
    message="Hi, I'm ready for my consultation."
)

if result['success']:
    print("WhatsApp opened. Click call button to start.")
    print(f"Call link: {result['call_link']}")
```

### 8. Schedule WhatsApp Call

```python
from whatsapp_caller import CallScheduler
from datetime import datetime, timedelta

scheduler = CallScheduler()

# Schedule call 30 minutes from now
call_time = datetime.now() + timedelta(minutes=30)

result = scheduler.add_scheduled_call(
    call_id="call_123",
    call_time=call_time,
    phone_number="+977XXXXXXXXXX",
    astrologer_name="Astrologer Name",
    duration_minutes=30
)

print(f"Call scheduled at: {result['scheduled_time']}")

# Later, check for due reminders
reminders = scheduler.get_due_reminders()
for reminder in reminders:
    print(f"Send {reminder['type']} reminder for {reminder['call_data']['astrologer']}")
```

### 9. Send WhatsApp Message (Twilio)

```python
from whatsapp_caller import TwilioWhatsAppCaller
import os
from dotenv import load_dotenv

load_dotenv()

caller = TwilioWhatsAppCaller(
    account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
    auth_token=os.getenv('TWILIO_AUTH_TOKEN'),
    twilio_whatsapp_number=os.getenv('TWILIO_WHATSAPP_NUMBER')
)

result = caller.send_whatsapp_notification(
    recipient_number="+977XXXXXXXXXX",
    message="Your astrology consultation starts in 15 minutes!"
)

if result['success']:
    print(f"Message sent: {result['message_id']}")
```

### 10. Generate Transaction Report

```python
from enhanced_payment_system import EnhancedPaymentSystem

system = EnhancedPaymentSystem()

report = system.export_transaction_report(user_id="user123")
print(report)

# Output example:
# TRANSACTION REPORT - user123
# Current Wallet Balance: NPR 200.00
# 
# Transaction ID: abc-123-def
# Amount: NPR 500.00
# Gateway: khalti
# Status: completed
# Date: 2025-12-07T10:30:00
# Purpose: wallet_topup
```

## Common Amounts (in paisa)

```python
# Khalti uses paisa (100 paisa = 1 NPR)
100 paisa = NPR 1
1000 paisa = NPR 10
5000 paisa = NPR 50
10000 paisa = NPR 100
50000 paisa = NPR 500
100000 paisa = NPR 1000
300000 paisa = NPR 3000
```

## Phone Number Formats

```python
# All supported formats:
"+977XXXXXXXXXX"    # With country code
"977XXXXXXXXXX"     # Without +
"XXXXXXXXXX"        # Local (auto adds +977)

# Examples:
"+977-9841234567"
"00977-9841234567"
"9841234567"
```

## Testing Credentials Summary

| Gateway | Status | Username | Password | Card |
|---------|--------|----------|----------|------|
| Khalti | Ready | - | - | 4111111111111111 |
| eSewa | Ready | test@esewa.com.np | asdf | N/A |
| PayPal | Ready | sb-buyer123... | - | N/A |
| Stripe | Ready | - | - | 4242424242424242 |

## Error Handling

```python
# Check for errors in response
result = gateway.initiate_payment(...)

if not result['success']:
    error = result.get('error', 'Unknown error')
    print(f"Payment failed: {error}")
    # Fallback options:
    # 1. Retry with different gateway
    # 2. Show wallet topup option
    # 3. Reschedule for later
```

## File Locations

```
Key Files:
- Payment Config: real_payment_gateway.py
- Wallet System: enhanced_payment_system.py
- WhatsApp: whatsapp_caller.py
- Instructions: SETUP_INSTRUCTIONS.md
- Summary: IMPLEMENTATION_SUMMARY.md
- This Guide: QUICK_REFERENCE.md

Data Files:
- Transactions: transactions.json (auto-created)
- .env: (create in Astrologers/ folder)
```

## Debugging

```python
# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check transaction data
system = EnhancedPaymentSystem()
history = system.get_transaction_history("user123")
print(json.dumps(history, indent=2, default=str))

# Verify gateway connectivity
gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.KHALTI)
print(f"Gateway base URL: {gateway.base_url}")
print(f"Test mode: {gateway.test_mode}")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "API key error" | Check .env file exists and has correct keys |
| "Connection refused" | Check internet, verify gateway domain |
| "WhatsApp not opening" | Try manual link: `print(result['call_link'])` |
| "Balance insufficient" | Top up wallet first |
| "Transaction not found" | Check transaction_id spelling |

---

**Ready to use! Start with Example 1 to test Khalti integration.**
