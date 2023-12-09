from apps.users.models import User
from apps.network.models import Network
from apps.invest.models import Invest
from apps.withdraw.models import Withdraw


def report_sub_invest(email):
    main_total_invest = 0
    main_total_active_invest = 0
    main_total_accepted = 0
    main_total_rejected = 0
    main_total_pending = 0

    main_user = User.objects.get(email=email)
    main_network = Network.objects.get(user=main_user)
    main_binary_place = main_network.binary_place

    sub_network_list = Network.objects.filter(
        binary_place__istartswith=main_binary_place,
    )

    with open('output.txt', 'w') as file:
        for network in sub_network_list:
            sub_total_invest = 0
            sub_total_active_invest = 0
            sub_total_accepted = 0
            sub_total_rejected = 0
            sub_total_pending = 0

            sub_user = network.user

            invest_list = Invest.objects.filter(
                user=sub_user,
            )

            for invest in invest_list:
                sub_total_invest += invest.package.price

                if invest.finished == False:
                    sub_total_active_invest += invest.package.price

            withdraw_list = Withdraw.objects.filter(
                user=sub_user,
            )

            for withdraw in withdraw_list:
                if withdraw.status == 'rejected':
                    sub_total_rejected += withdraw.amount

                elif withdraw.status == 'accepted':
                    sub_total_accepted += withdraw.amount

                elif withdraw.status == 'pending':
                    sub_total_pending += withdraw.amount

            main_total_invest += sub_total_invest
            main_total_active_invest += sub_total_active_invest
            main_total_accepted += sub_total_accepted
            main_total_rejected += sub_total_rejected
            main_total_pending += sub_total_pending

            print('Email:', end=' ', file=file)
            print(sub_user.email, file=file)

            print('Invest:', end=' ', file=file)
            print(sub_total_invest, file=file)

            print('Active Invest:', end=' ', file=file)
            print(sub_total_active_invest, file=file)

            print('Accepted:', end=' ', file=file)
            print(sub_total_accepted, file=file)

            print('Rejected', end=' ', file=file)
            print(sub_total_rejected, file=file)

            print('Pending', end=' ', file=file)
            print(sub_total_pending, file=file)

            print('====================', file=file)

        print('********************', file=file)
        print('FINAL RESULT', file=file)

        print('Main Email:', end=' ', file=file)
        print(main_user.email, file=file)

        print('Invest:', end=' ', file=file)
        print(main_total_invest, file=file)

        print('Active Invest', end=' ', file=file)
        print(main_total_active_invest, file=file)

        print('Accepted:', end=' ', file=file)
        print(main_total_accepted, file=file)

        print('Rejected', end=' ', file=file)
        print(main_total_rejected, file=file)

        print('Pending', end=' ', file=file)
        print(main_total_pending, file=file)

        print('********************', file=file)
