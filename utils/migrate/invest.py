import os
import datetime
import mysql.connector
import decimal

from apps.invest.models import Invest

from apps.users.models import User

from apps.package.models import Package

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, user_id, package_id, invest, total_invest, profit, payout_binary_status, payout_direct_status, finished, calculated_at, created_at, updated_at, deleted_at from invests"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    user_id = row[1]
    package_id = row[2]
    invest = row[3]
    total_invest = row[4]
    profit = row[5]
    payout_binary_status = row[6]
    payout_direct_status = row[7]
    finished = row[8]
    calculated_at = row[9]
    created_at = row[10]
    updated_at = row[11]
    deleted_at = row[12]

    # Find Package and User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None

    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        package = None

    # Convert invest, total_invest, profit to decimal
    invest = decimal.Decimal(invest)
    total_invest = decimal.Decimal(total_invest)
    profit = decimal.Decimal(profit)

    # Check payout_binary_status to set True or False
    if payout_binary_status == 0:
        payout_binary_status = False
    else:
        payout_binary_status = True

    # Check payout_direct_status to set True or False
    if payout_direct_status == 0:
        payout_direct_status = False
    else:
        payout_direct_status = True

    # Check finished to set True or False
    if finished == 0:
        finished = False
    else:
        finished = True

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    # Check calculated_at, created_at, updated_at, deleted_at
    if calculated_at:
        calculated_at = datetime.datetime.strptime(
            str(calculated_at),
            date_format,
        )

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    if deleted_at:
        deleted_at = datetime.datetime.strptime(str(deleted_at), date_format)

    invest_obj = Invest.objects.create(
        id=id,
        user=user,
        package=package,
        invest=invest,
        total_invest=total_invest,
        profit=profit,
        payout_binary_status=payout_binary_status,
        payout_direct_status=payout_direct_status,
        finished=finished,
        calculated_at=calculated_at,
        deleted_at=deleted_at,
        created_at=created_at,
        updated_at=updated_at,
    )
