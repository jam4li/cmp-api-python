import os
import datetime
import mysql.connector
import pytz
import decimal

from apps.users.models import User
from apps.network.models import NetworkTransaction
from apps.invest.models import Invest

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

cmd = "select id, user_id, invest_id, type, amount, day, description, created_at, updated_at, deleted_at from network_transactions"

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
        invest_id = row[2]
        type = row[3]
        amount = row[4]
        day = row[5]
        description = row[6]
        created_at = row[7]
        updated_at = row[8]
        deleted_at = row[9]

        try:
            user = User.objects.get(id=user_id)
            invest = Invest.objects.get(id=invest_id)
        except User.DoesNotExist:
            print('User not found')
            continue
        except Invest.DoesNotExist:
            print('Invest not found')
            print(user.email)
            continue

        if updated_at is None:
            updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            network_transaction_obj = NetworkTransaction.objects.select_related(
                'user',
                'invest',
            ).get(id=id)

        except NetworkTransaction.DoesNotExist:
            network_transaction_obj = NetworkTransaction(id=id)
            new_objects.append(network_transaction_obj)

        network_transaction_obj.user = user
        network_transaction_obj.invest = invest
        network_transaction_obj.type = type
        network_transaction_obj.amount = amount
        network_transaction_obj.day = day
        network_transaction_obj.description = description
        network_transaction_obj.created_at = created_at
        network_transaction_obj.updated_at = updated_at
        network_transaction_obj.deleted_at = deleted_at

        existing_objects.append(network_transaction_obj)

    if len(new_objects) > 5000:
        NetworkTransaction.objects.bulk_create(new_objects)
        print(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        NetworkTransaction.objects.bulk_update(
            existing_objects, [
                'user',
                'invest',
                'type',
                'amount',
                'day',
                'description',
                'created_at',
                'updated_at',
                'deleted_at',
            ],
        )
        print(existing_objects)
        existing_objects = []

    print(new_objects)
    print(existing_objects)

if new_objects:
    NetworkTransaction.objects.bulk_create(new_objects)

if existing_objects:
    NetworkTransaction.objects.bulk_update(
        existing_objects,
        [
            'user',
            'invest',
            'type',
            'amount',
            'day',
            'description',
            'created_at',
            'updated_at',
            'deleted_at',
        ],
    )
