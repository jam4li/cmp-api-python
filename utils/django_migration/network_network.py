import os
import mysql.connector

from apps.network.models import Network
from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, status, left_count, right_count, left_amount, right_amount, invest, last_invest, network_profit_daily_limit, network_profit, network_calculate_date, referrer_id, user_id, created_at, updated_at from networks"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    status = row[1]
    left_count = row[2]
    right_count = row[3]
    left_amount = row[4]
    right_amount = row[5]
    invest = row[6]
    last_invest = row[7]
    network_profit_daily_limit = row[8]
    network_profit = row[9]
    network_calculate_date = row[10]
    referrer_id = row[11]
    user_id = row[12]
    created_at = row[13]
    updated_at = row[14]

    # Check status to set True or False
    if status == 0:
        status = False
    else:
        status = True

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    try:
        referrer = User.objects.get(id=referrer_id)
    except User.DoesNotExist:
        referrer = None

    network_obj = Network.objects.create(
        id=id,
        status=status,
        left_count=left_count,
        right_count=right_count,
        left_amount=left_amount,
        right_amount=right_amount,
        invest=invest,
        last_invest=last_invest,
        network_profit_daily_limit=network_profit_daily_limit,
        network_profit=network_profit,
        network_calculate_date=network_calculate_date,
        referrer=referrer,
        user=user,
    )
