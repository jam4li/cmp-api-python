import os
import mysql.connector

from apps.wallet.models import Wallet
from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, title, type, access_type, balance, blocked_amount, user_id, created_at, updated_at from wallets"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    title = row[1]
    type = row[2]
    access_type = row[3]
    balance = row[4]
    blocked_amount = row[5]
    user_id = row[6]
    created_at = row[7]
    updated_at = row[8]

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    wallet_obj = Wallet.objects.create(
        id=id,
        title=title,
        type=type,
        access_type=access_type,
        balance=balance,
        blocked_amount=blocked_amount,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
