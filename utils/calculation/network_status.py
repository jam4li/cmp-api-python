# This script is designed to calculate the network status of users based on their invited users' investment activities.
# The script iterates through the Network model instances, representing the network relationships between users.
# The criteria for determining the network status are related to the presence of
# at least one active package in the left direct-invited user and one active package in the right-invited user.

from apps.network.models import Network
from apps.users.models import User
from apps.invest.models import Invest


def calculate_network_status():
    network_list = Network.objects.all()

    for network in network_list:
        print(network.id)
        user = network.user
        is_right_active = False
        is_left_active = False

        referral_network_list = Network.objects.filter(referrer=user)

        for referral_network in referral_network_list:
            referrer_user = referral_network.user
            active_invest_list = Invest.objects.filter(
                user=referrer_user,
                finished=False,
            )

            if active_invest_list:
                if referral_network.side == 'right':
                    is_right_active = True
                    continue

                elif referral_network.side == 'left':
                    is_left_active = True
                    continue

        if is_left_active and is_right_active:
            network.status = True
            network.save()
