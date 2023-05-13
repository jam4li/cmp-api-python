import os
import datetime
import mysql.connector
import decimal

from apps.withdraw.models import Withdraw

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

cmd = "select id, user_id, amount, fee, wallet_address, transaction_hash, status, wallet_type, created_at, updated_at from withdraws"

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
        amount = row[2]
        fee = row[3]
        wallet_address = row[4]
        transaction_hash = row[5]
        status = row[6]
        wallet_type = row[7]
        created_at = row[8]
        updated_at = row[9]

        # Find and User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            continue

        if created_at is None:
            created_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        if updated_at is None:
            updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            withdraw_obj = Withdraw.objects.get(id=id)

        except Withdraw.DoesNotExist:
            withdraw_obj = Withdraw(id=id)
            new_objects.append(withdraw_obj)

        withdraw_obj.user = user
        withdraw_obj.amount = amount
        withdraw_obj.fee = fee
        withdraw_obj.wallet_address = wallet_address
        withdraw_obj.transaction_hash = transaction_hash
        withdraw_obj.status = status
        withdraw_obj.wallet_type = wallet_type
        withdraw_obj.created_at = created_at
        withdraw_obj.updated_at = updated_at

        existing_objects.append(withdraw_obj)

    if len(new_objects) > 5000:
        Withdraw.objects.bulk_create(new_objects)
        print(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        Withdraw.objects.bulk_update(
            existing_objects, [
                'user',
                'amount',
                'fee',
                'wallet_address',
                'transaction_hash',
                'status',
                'wallet_type',
                'created_at',
                'updated_at',
            ],
        )
        print(existing_objects)
        existing_objects = []

    print(new_objects)
    print(existing_objects)

if new_objects:
    Withdraw.objects.bulk_create(new_objects)

if existing_objects:
    Withdraw.objects.bulk_update(
        existing_objects,
        [
            'user',
            'amount',
            'fee',
            'wallet_address',
            'transaction_hash',
            'status',
            'wallet_type',
            'created_at',
            'updated_at',
        ],
    )
