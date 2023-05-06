import os
import mysql.connector

from apps.withdraw.models import Withdraw
from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, amount, fee, wallet_address, transaction_hash, status, wallet_type, user_id, created_at, updated_at from withdraws"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    amount = row[1]
    fee = row[2]
    wallet_address = row[3]
    transaction_hash = row[4]
    status = row[5]
    wallet_type = row[6]
    user_id = row[7]
    created_at = row[8]
    updated_at = row[9]

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    withdraw_obj = Withdraw.objects.create(
        id=id,
        amount=amount,
        fee=fee,
        wallet_address=wallet_address,
        transaction_hash=transaction_hash,
        status=status,
        wallet_type=wallet_type,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
