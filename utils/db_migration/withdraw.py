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

cmd = "select id, user_id, amount, fee, wallet_address, transaction_hash, status, wallet_type, created_at, updated_at from withdraws"

cursor.execute(cmd)

records = cursor.fetchall()

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

    # Convert amount, fee
    amount = decimal.Decimal(amount)
    fee = decimal.Decimal(fee)

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    invest_obj = Withdraw.objects.create(
        id=id,
        user=user,
        amount=amount,
        fee=fee,
        wallet_address=wallet_address,
        transaction_hash=transaction_hash,
        status=status,
        wallet_type=wallet_type,
        created_at=created_at,
        updated_at=updated_at,
    )
