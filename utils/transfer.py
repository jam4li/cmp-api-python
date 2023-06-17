from apps.users.models import User
from apps.referral.models import Referral
from apps.network.models import Network


def remove_last_character(string):
    if len(string) > 0:
        modified_string = string[:-1]
        return modified_string
    else:
        return string


def find_last_character(string):
    if len(string) > 0:
        last_character = string[-1]
        return last_character
    else:
        return None


def transfer(origin_user_email, end_point_user_email, side='left'):
    origin_user = User.objects.get(email=origin_user_email)
    end_point_user = User.objects.get(email=end_point_user_email)

    origin_referral = Referral.objects.get(user=origin_user)
    end_point_referral = Referral.objects.get(user=end_point_user)

    origin_binary_place = origin_referral.binary_place
    end_point_binary_place = end_point_referral.binary_place

    origin_network = Network.objects.get(user=origin_user)
    end_point_network = Network.objects.get(user=end_point_user)

    origin_parent_binary_place = origin_binary_place

    # Minus origin_referral_network.left_amount and right_amount from the above nodes
    while True:
        origin_last_character = find_last_character(
            origin_parent_binary_place,
        )

        origin_parent_binary_place = remove_last_character(
            origin_parent_binary_place,
        )

        print('Origin Parent Binary Place', end=' ')
        print(origin_parent_binary_place)

        print('Origin Last Character', end=' ')
        print(origin_last_character)

        try:
            origin_parent_referral = Referral.objects.get(
                binary_place=origin_parent_binary_place,
            )
        except Referral.DoesNotExist:
            break

        origin_parent_user = origin_parent_referral.user
        origin_parent_network = Network.objects.get(
            user=origin_parent_user,
        )

        if origin_last_character == '0':
            print('Left')
            print('Origin Parent Network Left Count:', end=' ')
            print(origin_parent_network.left_count)
            print('Origin Parent Network Left Amount:', end=' ')
            print(origin_parent_network.left_amount)
            origin_parent_network.left_count -= 1
            origin_parent_network.left_amount -= origin_network.left_amount

        elif origin_last_character == '1':
            print('Right')
            print('Origin Parent Network Right Count:', end=' ')
            print(origin_parent_network.right_count)
            print('Origin Parent Network Right Amount:', end=' ')
            print(origin_parent_network.right_amount)
            origin_parent_network.right_count -= 1
            origin_parent_network.right_amount -= origin_network.right_amount

    # Plus origin_referral_network.left_amount and right_amount to the new above nodes
    while True:
        if side == 'left':
            new_origin_binary_place = end_point_binary_place + '0'

        elif side == 'right':
            new_origin_binary_place = end_point_binary_place + '1'

        new_origin_last_character = find_last_character(
            new_origin_parent_binary_place,
        )

        new_origin_parent_binary_place = remove_last_character(
            new_origin_parent_binary_place,
        )

        if new_origin_last_character == '0':
            print('Left')
            print('New Origin Parent Network Left Count:', end=' ')
            print(origin_parent_network.left_count)
            print('New Origin Parent Network Left Amount:', end=' ')
            print(origin_parent_network.left_amount)
            origin_parent_network.left_count -= 1
            origin_parent_network.left_amount -= origin_network.left_amount

        elif new_origin_last_character == '1':
            print('Right')
            print('New Origin Parent Network Right Count:', end=' ')
            print(origin_parent_network.right_count)
            print('New Origin Parent Network Right Amount:', end=' ')
            print(origin_parent_network.right_amount)
            origin_parent_network.right_count -= 1
            origin_parent_network.right_amount -= origin_network.right_amount

    # TODO: Calculate new binary_place for all of the users in the origin_user tree based on the end_point_user tree
