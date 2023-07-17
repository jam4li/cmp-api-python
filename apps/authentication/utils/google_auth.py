import os
import json
import jwt

from django.conf import settings

from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow


def read_client_config(file_path):
    with open(file_path) as config_file:
        config_data = json.load(config_file)
    return config_data


def create_google_url(side=None, referrer_code=None):
    google_auth_file_path = os.path.join(settings.BASE_DIR, 'google-auth.json')

    flow = Flow.from_client_config(
        client_config=read_client_config(google_auth_file_path),
        scopes=[
            'https://www.googleapis.com/auth/userinfo.email',
            'openid',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
        redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
    )

    if side and referrer_code:
        authorization_url, state = flow.authorization_url(
            state=f"side={side}&referrer_code={referrer_code}"
        )

    else:
        authorization_url, state = flow.authorization_url()

    return authorization_url


def callback_google(request):
    google_auth_file_path = os.path.join(settings.BASE_DIR, 'google-auth.json')

    flow = Flow.from_client_config(
        client_config=read_client_config(google_auth_file_path),
        scopes=[
            'https://www.googleapis.com/auth/userinfo.email',
            'openid',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
        state=request.GET['state'],
        redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
    )

    # Exchange the authorization code for an access token and a refresh token
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Get the state parameter value from the callback URL
    state_data = request.GET.get('state')

    side = None
    referrer_code = None

    if state_data:
        state_parts = state_data.split('&')
        for part in state_parts:
            key_value = part.split('=')
            if len(key_value) == 2:
                key, value = key_value
                if key == 'side':
                    side = value
                elif key == 'referrer_code':
                    referrer_code = value

    # Development mode
    if os.environ.get('OAUTHLIB_INSECURE_TRANSPORT') == '1':
        # Get the user's credentials (access token and refresh token)
        credentials = flow.credentials

        # Check if the _id_token attribute exists in the credentials object
        if hasattr(credentials, '_id_token'):
            # Get the user's ID token
            id_token_str = credentials._id_token
        else:
            # Raise an exception or handle the error as needed
            raise ValueError("ID token not found in the credentials object")

        # Convert the ID token to bytes
        id_token_bytes = id_token_str.encode('utf-8')

        # Use the following line in development only
        id_info = jwt.decode(
            id_token_bytes,
            options={"verify_signature": False},
        )

        id_info['side'] = side
        id_info['referrer_code'] = referrer_code

        return id_info

    # Production or Staging mode
    else:
        # Get the user's credentials (access token and refresh token)
        credentials = flow.credentials

        # Verify the ID token and fetch the user's profile information
        id_info = id_token.verify_oauth2_token(credentials.id_token, Request())

        return id_info
