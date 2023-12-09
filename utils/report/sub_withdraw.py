import datetime
from apps.network.models import Network
from apps.withdraw.models import Withdraw


def report_sub_withdraw():
    network_list = Network.objects.filter(
        binary_place__istartswith='00000000000100000000000',
    )

    total_withdraw = 0.0

    for network in network_list:
        user = network.user
        withdraw_list = Withdraw.objects.filter(
            user=user,
            status='pending',
            created_at__gte=datetime.date(2022, 10, 1),
            created_at__lt=datetime.date(2023, 4, 1),
        )

        for withdraw in withdraw_list:
            total_withdraw += withdraw.amount

    print(total_withdraw)
