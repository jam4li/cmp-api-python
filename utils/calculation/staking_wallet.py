import os
import mysql.connector
from datetime import datetime, timedelta
from django.utils import timezone
from apps.users.models import User
from apps.invest.models import Invest
from apps.wallet.models import Wallet

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor(buffered=True)

cursor.execute("SET GLOBAL wait_timeout = 28800")
cursor.execute("SET GLOBAL interactive_timeout = 28800")
cursor.execute("SET SESSION net_read_timeout=28800")
cursor.execute("SET SESSION net_write_timeout=28800")


def calculate_period(first_date, end_date):
    # Calculate the initial difference in days
    delta = end_date - first_date
    total_days = delta.days + 1

    current_date = first_date

    for day in range(delta.days + 1):
        # 5 is Saturday, 6 is Sunday
        if current_date.weekday() in [5, 6]:
            total_days -= 1

        current_date += timedelta(days=1)

    return total_days


def calculate_staking_first():
    first_end_date = datetime(2023, 1, 5)
    first_start_date = first_end_date - timedelta(days=433)

    second_end_date = datetime(2023, 3, 10)
    second_start_date = datetime(2023, 1, 6)

    third_end_date = datetime(2023, 10, 16)
    third_start_date = datetime(2023, 3, 11)

    user_list = User.objects.all()

    for user in user_list:
        print(user.id)
        profit_wallet_balance = 0

        cmd = "select wallet_id from user_wallet where user_id=" + str(user.id)
        cursor.execute(cmd)
        user_wallet_records = cursor.fetchall()

        for row in user_wallet_records:
            wallet_id = row[0]

            cmd = "select type, balance from wallets where id=" + \
                str(wallet_id)

            wallet_cursor = mydb.cursor(buffered=True)
            wallet_cursor.execute(cmd)
            wallets_records = wallet_cursor.fetchone()
            wallet_cursor.close()

            wallet_type = wallets_records[0]

            if wallet_type == 'profit':
                profit_wallet_balance = wallets_records[1]
                break

        total_invest = 0
        total_profit = 0

        invest_list = Invest.objects.filter(
            user=user,
            created_at__range=(first_start_date, third_end_date),
            updated_at__gt=second_end_date,
        )

        for invest in invest_list:
            invest_created_at = invest.created_at
            # Calculate from 2021-12-01 to 2023-01-05

            invest_created_at = invest_created_at.replace(tzinfo=None)

            if first_start_date <= invest_created_at <= first_end_date:
                total_invest += invest.invest

                first_period = calculate_period(
                    invest_created_at,
                    first_end_date,
                )

                second_period = calculate_period(
                    second_start_date,
                    second_end_date,
                )

                profit = (0.63 * float(invest.invest)) / 100
                invest_profit = profit * first_period

                profit = (0.5 * float(invest.invest)) / 100
                invest_profit += profit * second_period

                total_profit += invest_profit

            elif second_start_date <= invest_created_at <= second_end_date:
                total_invest += invest.invest

                first_period = calculate_period(
                    invest_created_at,
                    second_end_date,
                )

                profit = (0.5 * float(invest.invest)) / 100

                invest_profit = profit * first_period

                total_profit += invest_profit

        taken_amount = total_profit - float(profit_wallet_balance)
        staking_amount = float(total_invest) - (taken_amount / 2)

        staking_wallet = Wallet.objects.get(
            user=user,
            type='staking',
        )

        staking_wallet.balance = staking_amount
        staking_wallet.save()


def calculate_staking_second():
    third_end_date = datetime(2023, 10, 16)
    third_start_date = datetime(2023, 3, 11)

    invest_list = Invest.objects.filter(
        created_at__range=(third_start_date, third_end_date),
    )

    for invest in invest_list:
        print(invest.id)

        staking_wallet = Wallet.objects.get(
            user=invest.user,
            type='staking',
        )

        staking_wallet_balance = staking_wallet.balance
        staking_wallet.balance = float(
            staking_wallet_balance + invest.invest
        )
        staking_wallet.save()
