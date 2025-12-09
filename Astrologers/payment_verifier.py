"""Minimal Flask server to verify Khalti and eSewa payments server-side.

Endpoints:
- POST /verify/khalti  -> JSON {"token": "...", "amount": 100}
- POST /verify/esewa   -> JSON {"pid": "...", "amt": 100}

This keeps provider secrets off the desktop client. Set environment variables:
- KHALTI_SECRET_KEY
- ESEWA_MERCHANT_CODE

Run with: `python payment_verifier.py`
"""

import os
import logging
from flask import Flask, request, jsonify

try:
    import requests
except Exception:
    requests = None

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/verify/khalti', methods=['POST'])
def verify_khalti():
    """Verify a Khalti checkout token server-side."""
    data = request.get_json() or {}
    token = data.get('token')
    amount = data.get('amount')

    if not token or not amount:
        return jsonify({'success': False, 'error': 'token and amount are required'}), 400

    secret = os.environ.get('KHALTI_SECRET_KEY')
    if not secret:
        return jsonify({'success': False, 'error': 'KHALTI_SECRET_KEY not configured on server'}), 500

    if not requests:
        return jsonify({'success': False, 'error': 'requests library is required on server'}), 500

    verify_url = 'https://khalti.com/api/v2/payment/verify/'
    headers = {'Authorization': f'Key {secret}'}
    payload = {'token': token, 'amount': int(amount)}

    try:
        resp = requests.post(verify_url, data=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            return jsonify({'success': True, 'provider': 'khalti', 'response': body})
        else:
            return jsonify({'success': False, 'provider': 'khalti', 'status_code': resp.status_code, 'response': resp.text}), 502
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 502


@app.route('/verify/esewa', methods=['POST'])
def verify_esewa():
    """Perform a basic eSewa transaction record lookup. Requires merchant code (scd) and pid (payment id)."""
    data = request.get_json() or {}
    pid = data.get('pid')
    amt = data.get('amt')

    merchant = os.environ.get('ESEWA_MERCHANT_CODE')
    if not pid or not amt:
        return jsonify({'success': False, 'error': 'pid and amt are required'}), 400

    if not merchant:
        return jsonify({'success': False, 'error': 'ESEWA_MERCHANT_CODE not configured on server'}), 500

    if not requests:
        return jsonify({'success': False, 'error': 'requests library is required on server'}), 500

    # eSewa verification endpoint (may vary based on integration)
    verify_url = 'https://esewa.com.np/epay/transrec'
    params = {'pid': pid, 'scd': merchant, 'amt': amt}

    try:
        resp = requests.get(verify_url, params=params, timeout=10)
        if resp.status_code == 200:
            return jsonify({'success': True, 'provider': 'esewa', 'response': resp.text})
        else:
            return jsonify({'success': False, 'provider': 'esewa', 'status_code': resp.status_code, 'response': resp.text}), 502
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 502


if __name__ == '__main__':
    port = int(os.environ.get('PAYMENT_VERIFIER_PORT', '5001'))
    app.run(host='0.0.0.0', port=port, debug=False)
