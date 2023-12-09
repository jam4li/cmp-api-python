# This script is designed to calculate, for each user, the total investments made by
# all left and right direct-invited and binary-invited users within their network.

# NOTE: network_side_amount script is designed to calculate based on invest_id and
# network_side_amount_all is designed to calculate based on all networks.

from apps.invest.models import Invest
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


def calculate_side_amount(invest_id):
    invest = Invest.objects.get(id=invest_id)
    invest_user = invest.user
    amount = Invest.package.price

    invest_user_network = Network.objects.get(user=invest_user)
    invest_user_binary_place = invest_user_network.binary_place
    while True:
        if invest_user_binary_place == '':
            break

        last_character = find_last_character(
            invest_user_binary_place,
        )

        invest_user_binary_place = remove_last_character(
            invest_user_binary_place,
        )

        try:
            parent_network = Network.objects.get(
                binary_place=invest_user_binary_place,
            )
        except Network.DoesNotExist:
            continue

        if last_character == '0':
            parent_network.left_amount += amount

        elif last_character == '1':
            parent_network.right_amount += amount

        parent_network.save()
