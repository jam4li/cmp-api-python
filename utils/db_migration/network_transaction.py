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

# Sets wait_timeout to 8 hours
cursor.execute("SET GLOBAL wait_timeout = 28800")
# Sets interactive_timeout to 8 hours
cursor.execute("SET GLOBAL interactive_timeout = 28800")

cmd = "select id, user_id, invest_id, type, amount, day, description, created_at, updated_at, deleted_at from network_transactions"

cursor.execute(cmd)

while True:
    records = cursor.fetchmany(1000)

    new_objects = []
    existing_objects = []

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

        amount = decimal.Decimal(amount)

        # Change mysql's date to python's date
        date_format = '%Y-%m-%d %H:%M:%S'

        if created_at:
            created_at = datetime.datetime.strptime(
                str(created_at), date_format)
            created_at = created_at.replace(tzinfo=pytz.UTC)

        if updated_at:
            updated_at = datetime.datetime.strptime(
                str(updated_at), date_format)
            updated_at = updated_at.replace(tzinfo=pytz.UTC)

        if deleted_at:
            deleted_at = datetime.datetime.strptime(
                str(deleted_at), date_format)
            deleted_at = deleted_at.replace(tzinfo=pytz.UTC)

        try:
            network_transaction_obj = NetworkTransaction.objects.get(
                id=id,
            )

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

        except NetworkTransaction.DoesNotExist:
            network_transaction_obj = NetworkTransaction(
                id=id,
                user=user,
                invest=invest,
                type=type,
                amount=amount,
                day=day,
                description=description,
                created_at=created_at,
                updated_at=updated_at,
                deleted_at=deleted_at,
            )
            new_objects.append(network_transaction_obj)

    print(new_objects)
    print(existing_objects)

    NetworkTransaction.objects.bulk_create(new_objects)
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
