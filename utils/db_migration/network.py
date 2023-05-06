import os
import datetime
import mysql.connector
import decimal

from apps.network.models import Network

from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, user_id, status, left_count, right_count, left_amount, right_amount, invest, last_invest, network_profit_daily_limit, network_profit, referrer_id, network_calculate_date, created_at, updated_at from networks"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    user_id = row[1]
    status = row[2]
    left_count = row[3]
    right_count = row[4]
    left_amount = row[5]
    right_amount = row[6]
    invest = row[7]
    last_invest = row[8]
    network_profit_daily_limit = row[9]
    network_profit = row[10]
    referrer_id = row[11]
    network_calculate_date = row[12]
    created_at = row[13]
    updated_at = row[14]

    # Find Package and User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass

    # Check status to set True or False
    if status == 0:
        status = False
    else:
        status = True

    # Convert left_amount, right_amount, invest, last_invest, network_profit_daily_limit, network_profit
    left_amount = decimal.Decimal(left_amount)
    right_amount = decimal.Decimal(right_amount)
    invest = decimal.Decimal(invest)
    last_invest = decimal.Decimal(last_invest)
    network_profit_daily_limit = decimal.Decimal(network_profit_daily_limit)
    network_profit = decimal.Decimal(network_profit)

    try:
        referrer = User.objects.get(id=referrer_id)
    except User.DoesNotExist:
        referrer = None

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    # Check network_calculate_date, created_at, updated_at
    if network_calculate_date:
        network_calculate_date = datetime.datetime.strptime(
            str(network_calculate_date),
            date_format,
        )

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    invest_obj = Network.objects.create(
        id=id,
        user=user,
        status=status,
        left_count=left_count,
        right_count=right_count,
        left_amount=left_amount,
        right_amount=right_amount,
        invest=invest,
        last_invest=last_invest,
        network_profit_daily_limit=network_profit_daily_limit,
        network_profit=network_profit,
        referrer=referrer,
        network_calculate_date=network_calculate_date,
        created_at=created_at,
        updated_at=updated_at,
    )
