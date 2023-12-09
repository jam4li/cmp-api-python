from decimal import Decimal
from apps.network.models import Network


def calculate_all_network_side_amount():
    network_list = Network.objects.all()

    for network in network_list:
        left_amount = Decimal('0.0')
        right_amount = Decimal('0.0')

        network_binary_place = network.binary_place

        left_network_list = Network.objects.filter(
            binary_place__istartswith=network_binary_place + '0'
        )

        right_network_list = Network.objects.filter(
            binary_place__istartswith=network_binary_place + '1'
        )

        for left_network in left_network_list:
            left_amount += left_network.total_all_invest

        for right_network in right_network_list:
            right_amount += right_network.total_all_invest

        network.left_amount = left_amount
        network.right_amount = right_amount

        network.save()
