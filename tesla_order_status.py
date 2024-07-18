import os
import requests
import webbrowser
import urllib.parse

# Define constants
CLIENT_ID = 'ownerapi'
REDIRECT_URI = 'https://auth.tesla.com/void/callback'
AUTH_URL = 'https://auth.tesla.com/oauth2/v3/authorize'
TOKEN_URL = 'https://auth.tesla.com/oauth2/v3/token'
SCOPE = 'openid email offline_access'
CODE_CHALLENGE_METHOD = 'S256'
STATE = os.urandom(16).hex()


# Function to generate a code verifier and code challenge
def generate_code_verifier_and_challenge():
    import base64
    import hashlib
    import os

    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(
        b'=').decode('utf-8')
    return code_verifier, code_challenge


code_verifier, code_challenge = generate_code_verifier_and_challenge()

# Direct the user to the authentication page
auth_params = {
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'response_type': 'code',
    'scope': SCOPE,
    'state': STATE,
    'code_challenge': code_challenge,
    'code_challenge_method': CODE_CHALLENGE_METHOD,
}
auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"
print(f"Opening browser for authentication: {auth_url}")
webbrowser.open(auth_url)

# Get the redirected URL from the user
redirected_url = input("Please enter the redirected URL after authentication: ")
parsed_url = urllib.parse.urlparse(redirected_url)
auth_code = urllib.parse.parse_qs(parsed_url.query).get('code')[0]

# Exchange the authorization code for an access token
token_data = {
    'grant_type': 'authorization_code',
    'client_id': CLIENT_ID,
    'code': auth_code,
    'redirect_uri': REDIRECT_URI,
    'code_verifier': code_verifier,
}
response = requests.post(TOKEN_URL, data=token_data)
response.raise_for_status()
token_response = response.json()
access_token = token_response['access_token']

# Retrieve orders
headers = {
    'Authorization': f'Bearer {access_token}',
}
api_url = 'https://owner-api.teslamotors.com/api/1/users/orders'
response = requests.get(api_url, headers=headers)
response.raise_for_status()
orders_data = response.json()

for order in orders_data['response']:
    order_id = order['referenceNumber']
    print(
        f"Order ID: {order_id} | Status: {order['orderStatus']} | Model: {order['modelCode']} | VIN: {order.get('vin', 'N/A')}")
    api_url = f'https://akamai-apigateway-vfx.tesla.com/tasks?deviceLanguage=en&deviceCountry=DE&referenceNumber={order_id}&appVersion=4.32.6-2628'

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    api_data = response.json()

    # Print data
    scheduling = api_data.get('tasks', {}).get('scheduling', {})
    order = api_data.get('tasks', {}).get('registration', {}).get('orderDetails', {})

    print(f"Delivery Window: {scheduling.get('deliveryWindowDisplay', 'N/A')}")
    print(f"Vehicle Odometer: {order.get('vehicleOdometer', 'N/A')} {order.get('vehicleOdometerType', 'N/A')}")
    print(f"Delivery Appointment: {scheduling.get('apptDateTimeAddressStr', 'N/A')}")
