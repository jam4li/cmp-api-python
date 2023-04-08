import os
import datetime
import mysql.connector
import decimal

from apps.payment.models import Payment

from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, payment_hash, payment_code, amount, user_id, status, symbol, created_at, updated_at, charge from payments"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    payment_hash = row[1]
    payment_code = row[2]
    amount = row[3]
    user_id = row[4]
    status = row[5]
    symbol = row[6]
    created_at = row[7]
    updated_at = row[8]
    charge = row[9]

    # Find and User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    # Convert amount
    amount = decimal.Decimal(amount)

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    payment_obj = Payment.objects.create(
        id=id,
        payment_hash=payment_hash,
        payment_code=payment_code,
        amount=amount,
        user=user,
        status=status,
        symbol=symbol,
        charge=charge,
        created_at=created_at,
        updated_at=updated_at,
    )
