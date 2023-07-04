import os
import datetime
import mysql.connector
import decimal

from apps.transaction.models import Transaction

from apps.users.models import User
from apps.withdraw.models import Withdraw
from apps.payment.models import Payment

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, user_id, withdraw_id, payment_id, voucher_id, cmp_token_id, amount, type, status, description, created_at, updated_at from transactions"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    user_id = row[1]
    withdraw_id = row[2]
    payment_id = row[3]
    voucher_id = row[4]
    cmp_token_id = row[5]
    amount = row[6]
    type = row[7]
    status = row[8]
    description = row[9]
    created_at = row[10]
    updated_at = row[11]

    # Find and User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    try:
        withdraw = Withdraw.objects.get(id=withdraw_id)
    except Withdraw.DoesNotExist:
        withdraw = None

    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        payment = None

    # Convert amount
    amount = decimal.Decimal(amount)

    # Convert status
    if status == 0:
        status = False
    else:
        status = True

    transaction_obj = Transaction.objects.create(
        id=id,
        user=user,
        withdraw=withdraw,
        payment=payment,
        voucher=None,
        cmp_token=None,
        amount=amount,
        type=type,
        status=status,
        description=description,
        created_at=created_at,
        updated_at=updated_at,
    )
