import os
import datetime
import mysql.connector
import decimal

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

cursor = mydb.cursor()

cmd = "select id, user_id, wallet_id from user_wallet"

cursor.execute(cmd)

records = cursor.fetchall()

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
    cmd = "select id, title, type, access_type, balance, blocked_amount, created_at, updated_at from wallets where id=" + \
        str(wallet_id)
    cursor.execute(cmd)
    wallet = cursor.fetchone()

    wallet_id = wallet[0]
    wallet_title = wallet[1]
    wallet_type = wallet[2]
    wallet_access_type = wallet[3]
    wallet_balance = wallet[4]
    wallet_blocked_amount = wallet[5]
    wallet_created_at = wallet[6]
    wallet_updated_at = wallet[7]

    # Convert wallet_balance, wallet_blocked_amount to decimal
    wallet_balance = decimal.Decimal(wallet_balance)
    wallet_blocked_amount = decimal.Decimal(wallet_blocked_amount)

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if wallet_created_at:
        wallet_created_at = datetime.datetime.strptime(
            str(wallet_created_at), date_format)

    if wallet_updated_at:
        wallet_updated_at = datetime.datetime.strptime(
            str(wallet_updated_at), date_format)

    wallet_obj = Wallet.objects.create(
        id=wallet_id,
        user=user,
        title=wallet_title,
        type=wallet_type,
        access_type=wallet_access_type,
        balance=wallet_balance,
        blocked_amount=wallet_blocked_amount,
        created_at=wallet_created_at,
        updated_at=wallet_updated_at,
    )
