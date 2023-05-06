import os
import mysql.connector

from apps.invest.models import Invest
from apps.users.models import User
from apps.package.models import Package

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, invest, total_invest, profit, payout_binary_status, payout_direct_status, finished, calculated_at, deleted_at, package_id, user_id, created_at, updated_at from invests"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    invest = row[1]
    total_invest = row[2]
    profit = row[3]
    payout_binary_status = row[4]
    payout_direct_status = row[5]
    finished = row[6]
    calculated_at = row[7]
    deleted_at = row[8]
    package_id = row[9]
    user_id = row[10]
    created_at = row[11]
    updated_at = row[12]

    # Check status to set True or False
    if payout_binary_status == 0:
        payout_binary_status = False
    else:
        payout_binary_status = True

    if payout_direct_status == 0:
        payout_direct_status = False
    else:
        payout_direct_status = True

    if finished == 0:
        finished = False
    else:
        finished = True

    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        continue

    try:
        user = User.objects.get(id=user_id)
    except:
        continue

    invest_obj = Invest.objects.create(
        id=id,
        invest=invest,
        total_invest=total_invest,
        profit=profit,
        payout_binary_status=payout_binary_status,
        payout_direct_status=payout_direct_status,
        finished=finished,
        calculated_at=calculated_at,
        deleted_at=deleted_at,
        package=package,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
