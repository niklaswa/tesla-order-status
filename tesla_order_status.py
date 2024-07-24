import base64
import json
import os
import time
import hashlib
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
TOKEN_FILE = 'tesla_tokens.json'
ORDERS_FILE = 'tesla_orders.json'
APP_VERSION = '4.32.6-2628'


def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(
        b'=').decode('utf-8')
    return code_verifier, code_challenge


def get_auth_code():
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
    redirected_url = input("Please enter the redirected URL after authentication: ")
    parsed_url = urllib.parse.urlparse(redirected_url)
    return urllib.parse.parse_qs(parsed_url.query).get('code')[0]


def exchange_code_for_tokens(auth_code):
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response.raise_for_status()
    return response.json()


def save_tokens_to_file(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)
    print(f"Tokens saved to '{TOKEN_FILE}'")


def load_tokens_from_file():
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)


def is_token_valid(access_token):
    jwt_decoded = json.loads(base64.b64decode(access_token.split('.')[1] + '==').decode('utf-8'))
    return jwt_decoded['exp'] > time.time()


def refresh_tokens(refresh_token):
    token_data = {
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID,
        'refresh_token': refresh_token,
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response.raise_for_status()
    return response.json()


def retrieve_orders(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    api_url = 'https://owner-api.teslamotors.com/api/1/users/orders'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['response']


def get_order_details(order_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    api_url = f'https://akamai-apigateway-vfx.tesla.com/tasks?deviceLanguage=en&deviceCountry=DE&referenceNumber={order_id}&appVersion={APP_VERSION}'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()


def save_orders_to_file(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f)
    print(f"Orders saved to '{ORDERS_FILE}'")


def load_orders_from_file():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    return None


def compare_dicts(old_dict, new_dict, path=''):
    differences = []
    for key in old_dict:
        if key not in new_dict:
            differences.append(f"Removed key '{path + key}'")
        elif isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
            differences.extend(compare_dicts(old_dict[key], new_dict[key], path + key + '.'))
        elif old_dict[key] != new_dict[key]:
            differences.append(f"Changed value at '{path + key}': {old_dict[key]} -> {new_dict[key]}")

    for key in new_dict:
        if key not in old_dict:
            differences.append(f"Added key '{path + key}': {new_dict[key]}")

    return differences


def compare_orders(old_orders, new_orders):
    differences = []
    for i, old_order in enumerate(old_orders):
        if i < len(new_orders):
            differences.extend(compare_dicts(old_order, new_orders[i], path=f'Order {i}.'))
        else:
            differences.append(f"Removed order {i}")
    for i in range(len(old_orders), len(new_orders)):
        differences.append(f"Added order {i}")
    return differences


# Main script logic
code_verifier, code_challenge = generate_code_verifier_and_challenge()

if os.path.exists(TOKEN_FILE):
    try:
        token_file = load_tokens_from_file()
        access_token = token_file['access_token']
        refresh_token = token_file['refresh_token']

        if not is_token_valid(access_token):
            print("Access token is not valid. Refreshing tokens...")
            token_response = refresh_tokens(refresh_token)
            access_token = token_response['access_token']
            # refresh access token in file
            token_file['access_token'] = access_token
            save_tokens_to_file(token_file)

    except (json.JSONDecodeError, KeyError) as e:
        print("Error loading tokens from file. Re-authenticating...")
        token_response = exchange_code_for_tokens(get_auth_code())
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        save_tokens_to_file(token_response)
else:
    token_response = exchange_code_for_tokens(get_auth_code())
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    if input("Do you want to save the tokens to a file in the current directory? (y/n): ").lower() == 'y':
        save_tokens_to_file(token_response)

old_orders = load_orders_from_file()
new_orders = retrieve_orders(access_token)

# Retrieve detailed order information
detailed_new_orders = []
for order in new_orders:
    order_id = order['referenceNumber']
    order_details = get_order_details(order_id, access_token)
    detailed_order = {
        'order': order,
        'details': order_details
    }
    detailed_new_orders.append(detailed_order)

if old_orders:
    differences = compare_orders(old_orders, detailed_new_orders)
    if differences:
        print("Differences found:")
        for diff in differences:
            print(diff)
    else:
        print("No differences found.")

    save_orders_to_file(detailed_new_orders)
else:
    # ask user if they want to save the new orders to a file for comparison next time
    if input("Do you want to save the order information to a file for comparison next time? (y/n): ").lower() == 'y':
        save_orders_to_file(detailed_new_orders)

for detailed_order in detailed_new_orders:
    order = detailed_order['order']
    order_details = detailed_order['details']
    scheduling = order_details.get('tasks', {}).get('scheduling', {})
    order_info = order_details.get('tasks', {}).get('registration', {}).get('orderDetails', {})
    final_payment_data = order_details.get('tasks', {}).get('finalPayment', {}).get('data', {})

    print(f"Order ID: {order['referenceNumber']} | Status: {order['orderStatus']} | Model: {order['modelCode']} | VIN: {order.get('vin', 'N/A')}")
    print(f"Reservation Date: {order_info.get('reservationDate', 'N/A')}")
    print(f"Delivery Window: {scheduling.get('deliveryWindowDisplay', 'N/A')}")
    print(f"Vehicle Odometer: {order_info.get('vehicleOdometer', 'N/A')} {order_info.get('vehicleOdometerType', 'N/A')}")
    print(f"Vehicle Routing Location: {order_info.get('vehicleRoutingLocation', 'N/A')}")
    print(f"ETA to Delivery Center: {final_payment_data.get('etaToDeliveryCenter', 'N/A')}")
    print(f"Delivery Appointment: {scheduling.get('apptDateTimeAddressStr', 'N/A')}")
