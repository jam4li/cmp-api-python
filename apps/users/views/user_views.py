from django.conf import settings
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.response import ApiResponse
from apps.users.utils.google_auth import create_google_url, callback_google
from apps.users.utils.register import create_user

from apps.users.models import User, UserProfile
from apps.invest.models import Invest
from apps.wallet.models import Wallet
from apps.network.models import Network
# from .serializers import BannerListSerializer


class UserDashboardAPIView(views.APIView):
    """
    API view to fetch user's dashboard data.

    This view handles a GET request to retrieve the user's dashboard data.

    Returns:
        - A JSON response containing the user's dashboard data:
            - "active_packages" (int): The number of active investment packages the user has.
            - "balance" (float): The balance of staking wallet.
            - "direct_invited" (int): The count of users directly invited by the user (referrals).
            - "team" (int): The total size of the user's team in the binary tree structure.

    Note:
        - The "active_packages" count is calculated based on the Invest model, where 'finished' is False.
        - The "balance" is calculated by getting the balances of staking wallet belonging to the user.
        - The "direct_invited" count is based on the number of users in the Network model with the user as the referrer.
        - The "team" size is determined by summing up the counts of left and right children nodes in the binary tree.
    """

    def get(self, request, format=None):
        user = self.request.user

        # Calculate active packages
        active_packages = Invest.objects.filter(
            user=user,
            finished=False,
        ).count()

        # Calculate balance
        try:
            wallet = Wallet.objects.get(user=user, type='staking')
            balance = wallet.balance

        except Wallet.DoesNotExist:
            balance = 0

        direct_invited = Network.objects.filter(
            referrer=user,
        ).count()

        user_network = Network.objects.get(user=user)
        binary_right_count = user_network.right_count
        binary_left_count = user_network.left_count
        team = binary_right_count + binary_left_count

        data = {
            "active_packages": active_packages,
            "balance": balance,
            "direct_invited": direct_invited,
            "team": team,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class UserDetailAPIView(views.APIView):
    """
    API view to fetch user's email details.

    This view handles a GET request to retrieve the user's email details.

    Returns:
        - A JSON response containing the user's email:
            - "email" (str): The user's email address without the domain part.

    Note:
        - The user's email is extracted from the authenticated user's data.
        - The email domain part is omitted (e.g., '@gmail.com'), and only the local part is included in the response.
    """

    def get(self, request, format=None):
        user = self.request.user
        email = user.email.split('@')[0]
        data = {
            "email": email,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class UserCreateAPIView(views.APIView):
    """
    API view for creating a new user profile and generating a Gmail login link.

    This view handles a POST request to create a new user profile and generate a Gmail login link based on provided data.

    Parameters:
        - 'referrer' (str): The referrer's unique code for the user inviting the new user.
        - 'side' (str): The side on which the new user will be placed in the binary tree structure.

    Returns:
        - A JSON response containing the Gmail login link:
            - "url" (str): The generated Gmail login link for the new user.

    Note:
        - The API is designed to create a new user profile and generate a Gmail login link for the user.
        - The 'referrer' parameter is used to identify the referrer user in the database.
        - The 'side' parameter specifies the side (left or right) on which the new user will be placed in the binary tree.
        - The API verifies the existence of the referrer user based on the provided referrer code.
        - If the referrer user is not found in the database, the API returns an error response with a 404 status code.
        - If the referrer is found, the API creates a Gmail login link using the provided 'side' and referrer code.
        - The generated Gmail login link is returned in the response.
    """

    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        referrer_referrer_code = self.request.data['referrer']
        side = self.request.data['side']

        try:
            referrer_profile = UserProfile.objects.get(
                referrer_code=referrer_referrer_code,
            )
        except UserProfile.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'referrer_not_found',
                    'detail': 'Referrer user not found in the database',
                }
            )
            return Response(response)

        # Create gmail login link

        url = create_google_url(
            side=side,
            referrer_code=referrer_referrer_code,
        )

        # Create new user's profile

        return Response({'url': url})


class UserReferralDetailAPIView(views.APIView):
    """
    API view to fetch the referral code of the authenticated user.

    This view handles a GET request to retrieve the referral code of the authenticated user.

    Returns:
        - A JSON response containing the user's referral code:
            - "referrer_code" (str): The unique referral code associated with the user.

    Note:
        - The API fetches the authenticated user's profile using the provided user data.
        - The "referrer_code" represents the unique referral code associated with the user.
        - The referral code is used for inviting new users and tracking referrals in the system.
    """

    def get(self, request, format=None):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        data = {
            "referrer_code": user_profile.referrer_code,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class GoogleLogin(views.APIView):
    """
    API view to generate a Gmail login link.

    This view handles a GET request to generate a Gmail login link for user authentication.

    Returns:
        - A JSON response containing the Gmail login link:
            - "url" (str): The generated Gmail login link for user authentication.

    Note:
        - The API generates a Gmail login link to allow users to authenticate using their Gmail accounts.
        - The link is used to initiate the Gmail login process.
        - Users will be redirected to the Gmail login page, where they can log in with their Gmail credentials.
        - Upon successful authentication, users can grant permission to the website.
        - The website can then use the provided Gmail access token to access the user's Gmail data (if authorized).

    """

    permission_classes = [AllowAny, ]

    def get(self, request):
        url = create_google_url()
        return Response({'url': url})


class GoogleCallback(views.APIView):
    """
    API view to handle the callback from Google OAuth2 authentication.

    This view handles a GET request containing the callback data from Google OAuth2 authentication.
    The callback data is used to get_or_create a user and generate an authentication token.

    Parameters:
        - N/A (Note: The callback data is extracted from the request object directly.)

    Returns:
        - A redirect response to the user dashboard:
            - The user's dashboard is accessible through a frontend URL.
            - The redirect URL includes the authentication token and user email as query parameters.

    Note:
        - The API expects a callback from Google OAuth2 authentication, which provides user details such as email and name.
        - The API uses the received data to get_or_create a user in the system.
        - The 'side' and 'referrer_code' parameters, if present, are used to place the new user in the binary tree structure.
        - After creating the new user, the API generates an authentication token for the user.
        - The authentication token is included in the redirect URL to allow seamless authentication on the frontend.
        - The redirect URL leads to the user's dashboard, which is accessible through the frontend application.

    Redirect URL Format:
    ```
    https://FRONT_END_URL/dashboard/?token=<authentication_token>&email=<user_email>
    ```

    (Note: Replace <authentication_token> and <user_email> with the actual token and email data)

    Example Redirect URL:
    ```
    https://cm-enterprise.com/dashboard/?token=your_auth_token_here&email=user@example.com
    ```
    """

    permission_classes = [AllowAny, ]

    def get(self, request):
        id_info = callback_google(request)

        user_email = id_info['email']
        user_name = id_info['name']

        user_side = id_info['side']
        user_referrer_code = id_info['referrer_code']

        if user_side and user_referrer_code:
            create_user(
                email=user_email,
                side=user_side,
                referrer_code=user_referrer_code,
            )

        user = User.objects.get(email=user_email)
        token, created = Token.objects.get_or_create(user=user)

        front_end_url = settings.FRONT_END_URL

        redirect_url = front_end_url + "/dashboard/?token={0}&email={1}".format(
            token,
            user_email,
        )

        return redirect(redirect_url)


class Logout(views.APIView):
    """
    API view to handle user logout and revoke the authentication token.

    This view handles a GET request to revoke the authentication token of the authenticated user.

    Parameters:
        - N/A (Note: The authentication token is revoked based on the authenticated user.)

    Returns:
        - A response indicating the result of the logout process:
            - If the token is successfully revoked, a success message is returned with a 200 status code.
            - If the authenticated user is not found or has no associated token, an error message is returned with a 400 status code.

    Note:
        - The API expects a GET request to revoke the authentication token of the authenticated user.
        - The authentication token is obtained based on the authenticated user.
        - If a valid token is found for the user, it is deleted to revoke the authentication.
        - If the user is not found or has no associated token, an error message is returned.

    Example Success Response:
    ```
    HTTP 200 OK
    {
        "message": "User successfully logged out. Token revoked."
    }
    ```

    Example Error Response:
    ```
    HTTP 400 BAD REQUEST
    {
        "Error": "Could not find user with email: user@example.com"
    }
    ```
    """

    def get(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except User.DoesNotExist:
            return Response({"Error:": f"Could not find user with email:{request.user.email}"}, status=status.HTTP_400_BAD_REQUEST)
