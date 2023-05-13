import os
import datetime
import mysql.connector
import decimal
import pytz

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

cursor.execute("SET GLOBAL wait_timeout = 28800")
cursor.execute("SET GLOBAL interactive_timeout = 28800")
cursor.execute("SET SESSION net_read_timeout=28800")
cursor.execute("SET SESSION net_write_timeout=28800")

cmd = "select id, user_id, status, left_count, right_count, left_amount, right_amount, invest, last_invest, network_profit_daily_limit, network_profit, referrer_id, network_calculate_date, created_at, updated_at from networks"

cursor.execute(cmd)

existing_objects = []
new_objects = []

while True:
    records = cursor.fetchmany(1000)

    if not records:
        break

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

        try:
            referrer = User.objects.get(id=referrer_id)
        except User.DoesNotExist:
            referrer = None

        if created_at is None:
            created_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        if updated_at is None:
            updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            network_obj = Network.objects.get(id=id)

        except Network.DoesNotExist:
            network_obj = Network(id=id)
            new_objects.append(network_obj)

        network_obj.user = user
        network_obj.status = status
        network_obj.left_count = left_count
        network_obj.right_count = right_count
        network_obj.left_amount = left_amount
        network_obj.right_amount = right_amount
        network_obj.invest = invest
        network_obj.last_invest = last_invest
        network_obj.network_profit_daily_limit = network_profit_daily_limit
        network_obj.network_profit = network_profit
        network_obj.referrer = referrer
        network_obj.network_calculate_date = network_calculate_date
        network_obj.created_at = created_at
        network_obj.updated_at = updated_at

        existing_objects.append(network_obj)

    if len(new_objects) > 5000:
        Network.objects.bulk_create(new_objects)
        print(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        Network.objects.bulk_update(
            existing_objects, [
                'user',
                'status',
                'left_count',
                'right_count',
                'left_amount',
                'right_amount',
                'invest',
                'last_invest',
                'network_profit_daily_limit',
                'network_profit',
                'referrer',
                'network_calculate_date',
                'created_at',
                'updated_at',
            ],
        )
        print(existing_objects)
        existing_objects = []

    print(new_objects)
    print(existing_objects)

if new_objects:
    Network.objects.bulk_create(new_objects)

if existing_objects:
    Network.objects.bulk_update(
        existing_objects,
        [
            'user',
            'status',
            'left_count',
            'right_count',
            'left_amount',
            'right_amount',
            'invest',
            'last_invest',
            'network_profit_daily_limit',
            'network_profit',
            'referrer',
            'network_calculate_date',
            'created_at',
            'updated_at',
        ],
    )
