from apps.users.models import User
from apps.network.models import Network
from apps.wallet.models import Wallet


def report_sub_staking(email):
    file_name = email + '.txt'

    total_staking = 0

    main_user = User.objects.get(email=email)
    main_network = Network.objects.get(user=main_user)
    main_binary_place = main_network.binary_place

    sub_network_list = Network.objects.filter(
        binary_place__istartswith=main_binary_place,
    )

    with open(file_name, 'w') as file:
        for network in sub_network_list:
            sub_user = network.user

            staking_wallet = Wallet.objects.get(
                user=sub_user,
                type='staking',
            )

            staking_wallet_balance = staking_wallet.balance

            total_staking += staking_wallet_balance

            print(sub_user.email, end=': ', file=file)
            print(staking_wallet_balance, file=file)
            print('====================', file=file)

        print('********************', file=file)
        print('FINAL RESULT', file=file)

        print('Main Email:', end=' ', file=file)
        print(main_user.email, file=file)

        print('Total Staking:', end=' ', file=file)
        print(total_staking, file=file)

        print('********************', file=file)
