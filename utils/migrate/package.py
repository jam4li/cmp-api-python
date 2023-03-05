import os
import datetime
import mysql.connector

from package.models import Package

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, name, price, image, summery, status, fee, daily_profit, daily_profit_percent, profit_limit, created_at, updated_at from packages"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    name = row[1]
    price = row[2]
    summery = row[4]
    status = row[5]
    fee = row[6]
    daily_profit = row[7]
    daily_profit_percent = row[8]
    profit_limit = row[9]
    created_at = row[10]
    updated_at = row[11]

    # Check status to set True or False
    if status == 0:
        status = False
    else:
        status = True

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    package_obj = Package.objects.create(
        id=id,
        name=name,
        price=price,
        summery=summery,
        status=status,
        fee=fee,
        daily_profit=daily_profit,
        daily_profit_percent=daily_profit_percent,
        profit_limit=profit_limit,
        created_at=created_at,
        updated_at=updated_at,
    )
