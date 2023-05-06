import os
import datetime
import mysql.connector

from cmp.models import CMPClaimHistory

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, wallet, transaction_hash, amount, profit, total_claim, locked_at, unlocked_at, created_at, updated_at from cmp_claim_histories"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    wallet = row[1]
    transaction_hash = row[2]
    amount = row[3]
    profit = row[4]
    total_claim = row[5]
    locked_at = row[6]
    unlocked_at = row[7]
    created_at = row[8]
    updated_at = row[9]

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if locked_at:
        locked_at = datetime.datetime.strptime(str(locked_at), date_format)

    if unlocked_at:
        unlocked_at = datetime.datetime.strptime(str(unlocked_at), date_format)

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    cmp_claim_histories_obj = CMPClaimHistory.objects.create(
        id=id,
        wallet=wallet,
        transaction_hash=transaction_hash,
        amount=amount,
        profit=profit,
        total_claim=total_claim,
        locked_at=locked_at,
        unlocked_at=unlocked_at,
        created_at=created_at,
        updated_at=updated_at,
    )
