# Astrology Consultation System - Setup Instructions

## Overview
Complete payment gateway integration with WhatsApp calling for astrology consultations.

## Payment Gateways Supported

### 1. Khalti (Nepal)
**Status**: Sandbox/Test Mode Ready
**Website**: https://khalti.com

#### Setup:
1. Create account at https://merchant.khalti.com
2. Get credentials from Dashboard:
   - Public Key
   - Secret Key
3. Update in `real_payment_gateway.py`:
```python
self.public_key = "your_public_key"
self.secret_key = "your_secret_key"
```

#### Features:
- QR code generation for payments
- Phone number based transactions
- Test card: 4111111111111111
- Test OTP: 123456

#### Testing:
- Minimum: NPR 10
- Maximum: NPR 100,000 per transaction
- Test merchants get 1% fee

---

### 2. eSewa (Nepal)
**Status**: Sandbox/Test Mode Ready
**Website**: https://esewa.com.np

#### Setup:
1. Register at https://dev.esewa.com.np
2. Request test credentials
3. Update in `real_payment_gateway.py`:
```python
self.merchant_code = "EPAYTEST"  # or your code
self.merchant_key = "8gBm/:&EnhH.1/q"
```

#### Features:
- Form-based payment
- MD5 signature verification
- Email-based confirmation
- Support for installments

#### Testing:
- Test email: test@esewa.com.np
- Test password: asdf
- Test amounts: Any amount

---

### 3. PayPal
**Status**: Sandbox/Test Mode Ready
**Website**: https://developer.paypal.com

#### Setup:
1. Create sandbox account:
   - Go to https://developer.paypal.com
   - Create app in Sandbox
2. Get credentials:
   - Client ID
   - Client Secret
3. Update in `real_payment_gateway.py`:
```python
self.client_id = "your_sandbox_client_id"
self.client_secret = "your_sandbox_client_secret"
```

#### Test Accounts:
- Business: sb-w1234567890_api1.business.example.com
- Personal: sb-buyer123456789_personal.example.com

#### Features:
- Credit card support
- PayPal wallet
- International payments
- Webhooks for events

---

### 4. Stripe
**Status**: Sandbox/Test Mode Ready
**Website**: https://stripe.com

#### Setup:
1. Create account at https://dashboard.stripe.com
2. Go to Developers → API Keys
3. Copy test keys:
   - Publishable Key
   - Secret Key
4. Update in `real_payment_gateway.py`:
```python
self.api_key = "sk_test_your_test_key"
self.publishable_key = "pk_test_your_test_key"
```

#### Test Cards:
- Success: 4242 4242 4242 4242
- Fail: 4000 0000 0000 0002
- 3D Secure: 4000 0025 0000 3155

---

## WhatsApp Integration

### Method 1: Direct WhatsApp Links (Recommended)
**No API keys required**

When user calls:
1. Browser opens WhatsApp chat
2. User manually clicks call button
3. Direct peer-to-peer connection

#### Implementation:
```python
from whatsapp_caller import WhatsAppCaller

caller = WhatsAppCaller()
result = caller.initiate_whatsapp_call(
    phone_number="+977XXXXXXXXXX",
    astrologer_name="Astrologer Name",
    duration_minutes=30
)
```

### Method 2: Twilio WhatsApp (Optional)
**Requires API setup**

For automated notifications:

#### Setup:
1. Create account at https://www.twilio.com
2. Get WhatsApp Sandbox:
   - Account SID
   - Auth Token
   - WhatsApp Number
3. Update in `whatsapp_caller.py`:
```python
caller = TwilioWhatsAppCaller(
    account_sid="your_sid",
    auth_token="your_token",
    twilio_whatsapp_number="+1234567890"
)
```

#### Usage:
```python
result = caller.send_whatsapp_notification(
    recipient_number="+977XXXXXXXXXX",
    message="Your consultation is starting!"
)
```

---

## Installation

### 1. Install Dependencies
```bash
cd c:\Users\dines\OneDrive\Desktop\Kundali\Astrologers
pip install -r requirements.txt
```

### 2. Create Environment File (.env)
```
# Khalti
KHALTI_PUBLIC_KEY=your_public_key
KHALTI_SECRET_KEY=your_secret_key

# eSewa
ESEWA_MERCHANT_CODE=EPAYTEST
ESEWA_MERCHANT_KEY=8gBm/:&EnhH.1/q

# PayPal
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_secret

# Stripe
STRIPE_API_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx

# Twilio (Optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_NUMBER=+1234567890
```

### 3. Load Environment
```python
from dotenv import load_dotenv
import os

load_dotenv()
khalti_key = os.getenv('KHALTI_PUBLIC_KEY')
```

---

## Integration with main.py

### Updated Payment Flow:

1. **User selects astrologer and duration**
   - Choose payment method (Khalti, eSewa, PayPal, Stripe, Wallet)
   - See total amount with fees

2. **Payment Processing**
   - Direct to payment gateway
   - Show QR codes (Khalti)
   - Open payment forms (eSewa, PayPal)

3. **Payment Verification**
   - Webhook or callback handling
   - Update transaction status
   - Add to wallet (if topup)

4. **Call Initiation**
   - Open WhatsApp automatically
   - Show call timer
   - Log call history

### Example Code:
```python
from real_payment_gateway import PaymentGatewayFactory, PaymentGateway
from enhanced_payment_system import EnhancedPaymentSystem
from whatsapp_caller import WhatsAppCaller

# Create payment system
payment_system = EnhancedPaymentSystem()

# User selects Khalti
gateway = PaymentGatewayFactory.create_gateway(PaymentGateway.KHALTI, test_mode=True)

# Initiate payment
response = gateway.initiate_payment(
    amount=30000,  # NPR 300 in paisa
    phone="+977XXXXXXXXXX",
    product_name="30-min Astrology Consultation"
)

# After payment success
payment_system.verify_payment(transaction_id)

# Start WhatsApp call
whatsapp = WhatsAppCaller()
whatsapp.initiate_whatsapp_call(
    phone_number=astrologer_phone,
    astrologer_name=astrologer_name
)
```

---

## File Structure

```
Astrologers/
├── main.py (Updated with new payment system)
├── real_payment_gateway.py (All gateway integrations)
├── whatsapp_caller.py (WhatsApp & Twilio calling)
├── enhanced_payment_system.py (Wallet & transactions)
├── astrologers_data.py (Existing astrologer data)
├── call_handler.py (Existing call handling)
├── hindu_theme.py (Existing theme)
├── payment_gateway.py (Old - keep for compatibility)
├── payment_system.py (Old - keep for compatibility)
├── requirements.txt (Updated dependencies)
├── .env (Create this - add your API keys)
└── transactions.json (Auto-created for payment records)
```

---

## Testing Checklist

### Khalti Testing
- [ ] Generate QR code
- [ ] Scan with test phone
- [ ] Enter test OTP
- [ ] Verify payment completes
- [ ] Check wallet updated

### eSewa Testing
- [ ] Open payment form
- [ ] Enter test credentials
- [ ] Verify success redirect
- [ ] Check transaction logged

### PayPal Testing
- [ ] Click PayPal button
- [ ] Login with sandbox account
- [ ] Approve payment
- [ ] Verify return to app

### Stripe Testing
- [ ] Enter test card
- [ ] Complete payment
- [ ] Check success response
- [ ] Verify webhook handling

### WhatsApp Testing
- [ ] Click call button
- [ ] Verify WhatsApp opens
- [ ] Manual call connection
- [ ] Log call history

---

## Production Deployment

### Before Going Live:

1. **Switch to Live Keys**
   - Update all gateway credentials
   - Use production API endpoints
   - Enable security features

2. **SSL/TLS Certificates**
   - All payment pages must be HTTPS
   - Implement certificate pinning

3. **PCI Compliance**
   - Store minimal card data
   - Use tokenization
   - Never log sensitive data

4. **Backup & Recovery**
   - Daily transaction backups
   - Disaster recovery plan
   - Redundant payment gateways

5. **Monitoring**
   - Payment failure alerts
   - Transaction reconciliation
   - User support system

6. **Testing**
   - Load testing with real traffic
   - Security penetration testing
   - Payment flow edge cases

---

## Troubleshooting

### Khalti Issues
```
Error: "Public key not configured"
Solution: Check .env file and KHALTI_PUBLIC_KEY
```

### eSewa Issues
```
Error: "Invalid signature"
Solution: Verify merchant key and md5 encoding
```

### PayPal Issues
```
Error: "Invalid access token"
Solution: Regenerate client ID/secret in sandbox
```

### WhatsApp Issues
```
Error: "Browser could not open"
Solution: Check if webbrowser module available
         Try manual WhatsApp link approach
```

---

## Support

For issues:
1. Check logs in transactions.json
2. Review payment gateway test dashboards
3. Check internet connectivity
4. Verify API credentials in .env

---

## References

- Khalti Docs: https://docs.khalti.com/
- eSewa API: https://developer.esewa.com.np
- PayPal REST: https://developer.paypal.com/
- Stripe API: https://stripe.com/docs/
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: Ready for Testing
