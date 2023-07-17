import random
import string

from django.db import IntegrityError

from apps.users.models import User, UserProfile
from apps.referral.models import Referral
from apps.wallet.models import Wallet
from apps.network.models import Network


def generate_random_username(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_referrer_code(length=6):
    characters = string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


def create_user(email, side, referrer_code):
    referrer_profile = UserProfile.objects.get(
        referrer_code=referrer_code,
    )
    referrer_user = referrer_profile.user
    referrer_referral = Referral.objects.get(
        user=referrer_user,
    )
    referrer_binary_place = referrer_referral.binary_place

    new_binary_place = referrer_binary_place
    new_username = ""
    new_referrer_code = ""

    # Calculate new user's binary_place
    if side == 'left':
        while True:
            new_binary_place += "0"
            try:
                Referral.objects.get(binary_place=new_binary_place)
            except Referral.DoesNotExist:
                break

    elif side == 'right':
        while True:
            new_binary_place += "1"
            try:
                Referral.objects.get(binary_place=new_binary_place)
            except Referral.DoesNotExist:
                break

    # Generate username and check if username hasn't been taken before
    while True:
        new_username = generate_random_username()

        try:
            UserProfile.objects.get(username=new_username)
        except UserProfile.DoesNotExist:
            break

    # Generate referrer_code and check if username hasn't been taken before
    while True:
        new_referrer_code = generate_random_referrer_code()

        try:
            UserProfile.objects.get(referrer_code=new_referrer_code)
        except UserProfile.DoesNotExist:
            break

    # Create new user's User object
    try:
        new_user = User.objects.create(
            email=email,
        )
    except IntegrityError:
        return False

    new_user_profile = UserProfile.objects.create(
        user=new_user,
        username=new_username,
        referrer=referrer_profile,
        referrer_code=new_referrer_code,
        role='user',
    )

    # Create wallets based on types
    wallet_types = Wallet.TYPE_CHOICES
    for wallet_type, label in wallet_types:
        title = label + " " + "Wallet"
        Wallet.objects.create(
            user=new_user,
            title=title,
            type=wallet_type,
            access_type='user',
        )

     # Create network
    new_network = Network.objects.create(
        user=new_user,
        referrer=referrer_user,
    )

    # Create referral
    new_referral = Referral.objects.create(
        user=new_user,
        network=new_network,
        referrer=referrer_user,
        recruited=side,
        binary_place=new_binary_place,
    )

    # Calculate left_count or right_count in binary
    while len(new_binary_place) > 0:
        user_side = new_binary_place[-1]
        new_binary_place = new_binary_place[:-1]

        try:
            user_referral = Referral.objects.get(binary_place=new_binary_place)
            user = user_referral.user
            user_network = Network.objects.get(user=user)

            if user_side == '0':
                user_network.left_count = user_network.left_count + 1
                user_network.save()

            elif user_side == '1':
                user_network.right_count = user_network.right_count + 1
                user_network.save()

        except Referral.DoesNotExist:
            continue

        except Network.DoesNotExist:
            continue
