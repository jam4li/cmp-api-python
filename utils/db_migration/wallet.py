import os
import datetime
import mysql.connector
import decimal
import pytz

from apps.users.models import User
from apps.package.models import Package
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

cmd = "select id, user_id, wallet_id from user_wallet"

cursor.execute(cmd)

existing_objects = []
new_objects = []

batch_size = 10000
fetch_counter = 0

while True:
    records = cursor.fetchmany(batch_size)

    fetch_counter += batch_size
    print(fetch_counter)

    if not records:
        break

    for row in records:
        id = row[0]
        user_id = row[1]
        wallet_id = row[2]

        # Find users from user_id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            continue

        # Find wallet and retrieve data
        wallet_cursor = mydb.cursor(buffered=True)
        cmd = "select id, title, type, access_type, balance, blocked_amount, created_at, updated_at from wallets where id=" + \
            str(wallet_id)
        wallet_cursor.execute(cmd)
        wallet = wallet_cursor.fetchone()
        wallet_cursor.close()

        wallet_id = wallet[0]
        wallet_title = wallet[1]
        wallet_type = wallet[2]
        wallet_access_type = wallet[3]
        wallet_balance = wallet[4]
        wallet_blocked_amount = wallet[5]
        wallet_created_at = wallet[6]
        wallet_updated_at = wallet[7]

        if wallet_created_at is None:
            wallet_created_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        if wallet_updated_at is None:
            wallet_updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            wallet_obj = Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            wallet_obj = Wallet(id=wallet_id)
            new_objects.append(wallet_obj)

        wallet_obj.user = user
        wallet_obj.title = wallet_title
        wallet_obj.type = wallet_type
        wallet_obj.access_type = wallet_access_type
        wallet_obj.balance = wallet_balance
        wallet_obj.blocked_amount = wallet_blocked_amount
        wallet_obj.created_at = wallet_created_at
        wallet_obj.updated_at = wallet_updated_at

        existing_objects.append(wallet_obj)

    if len(new_objects) > 5000:
        Wallet.objects.bulk_create(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        Wallet.objects.bulk_update(
            existing_objects, [
                'user',
                'title',
                'type',
                'access_type',
                'balance',
                'blocked_amount',
                'created_at',
                'updated_at',
            ],
        )
        existing_objects = []


if new_objects:
    Wallet.objects.bulk_create(new_objects)

if existing_objects:
    Wallet.objects.bulk_update(
        existing_objects,
        [
            'user',
            'title',
            'type',
            'access_type',
            'balance',
            'blocked_amount',
            'created_at',
            'updated_at',
        ],
    )
