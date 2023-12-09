from apps.users.models import User, UserProfile
from apps.network.models import Network


def fix_register(email, side='left'):
    user = User.objects.get(email=email)
    user_profile = UserProfile.objects.get(user=user)

    referrer_profile = user_profile.referrer
    referrer_user = referrer_profile.user
    referrer_network = Network.objects.get(
        user=referrer_user,
    )

    referrer_binary_place = referrer_network.binary_place
    new_binary_place = referrer_binary_place

    # Calculate new user's binary_place
    if side == 'left':
        while True:
            new_binary_place += "0"
            try:
                Network.objects.get(binary_place=new_binary_place)
            except Network.DoesNotExist:
                break

    elif side == 'right':
        while True:
            new_binary_place += "1"
            try:
                Network.objects.get(binary_place=new_binary_place)
            except Network.DoesNotExist:
                break

    new_network = Network.objects.create(
        user=user,
        referrer=referrer_user,
        side=side,
        binary_place=new_binary_place,
    )

    # Calculate left_count or right_count in binary
    while len(new_binary_place) > 0:
        user_side = new_binary_place[-1]
        new_binary_place = new_binary_place[:-1]

        try:
            user_network = Network.objects.get(binary_place=new_binary_place)
            user = user_network.user

            if user_side == '0':
                user_network.left_count = user_network.left_count + 1
                user_network.save()

            elif user_side == '1':
                user_network.right_count = user_network.right_count + 1
                user_network.save()

        except Network.DoesNotExist:
            continue
