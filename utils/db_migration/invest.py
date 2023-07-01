import os
import datetime
import mysql.connector
import decimal
import pytz

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

cursor.execute("SET GLOBAL wait_timeout = 28800")
cursor.execute("SET GLOBAL interactive_timeout = 28800")
cursor.execute("SET SESSION net_read_timeout=28800")
cursor.execute("SET SESSION net_write_timeout=28800")

cmd = "select id, user_id, package_id, invest, total_invest, profit, payout_binary_status, payout_direct_status, finished, calculated_at, created_at, updated_at, deleted_at from invests"

cursor.execute(cmd)

existing_objects = []
new_objects = []

while True:
    records = cursor.fetchmany(1000)

    if not records:
        break

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
            package = Package.objects.get(id=package_id)
        except User.DoesNotExist:
            user = None
        except Package.DoesNotExist:
            package = None

        if created_at is None:
            created_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        if updated_at is None:
            updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            invest_obj = Invest.objects.get(id=id)

        except Invest.DoesNotExist:
            invest_obj = Invest(id=id)
            new_objects.append(invest_obj)

        invest_obj.user = user
        invest_obj.package = package
        invest_obj.invest = invest
        invest_obj.total_invest = total_invest
        invest_obj.profit = profit
        invest_obj.payout_binary_status = payout_binary_status
        invest_obj.payout_direct_status = payout_direct_status
        invest_obj.finished = finished
        invest_obj.calculated_at = calculated_at
        invest_obj.deleted_at = deleted_at
        invest_obj.created_at = created_at
        invest_obj.updated_at = updated_at

        existing_objects.append(invest_obj)

    if len(new_objects) > 5000:
        Invest.objects.bulk_create(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        Invest.objects.bulk_update(
            existing_objects, [
                'user',
                'package',
                'invest',
                'total_invest',
                'profit',
                'payout_binary_status',
                'payout_direct_status',
                'finished',
                'calculated_at',
                'deleted_at',
                'created_at',
                'updated_at',
            ],
        )
        existing_objects = []


if new_objects:
    Invest.objects.bulk_create(new_objects)

if existing_objects:
    Invest.objects.bulk_update(
        existing_objects,
        [
            'user',
            'package',
            'invest',
            'total_invest',
            'profit',
            'payout_binary_status',
            'payout_direct_status',
            'finished',
            'calculated_at',
            'deleted_at',
            'created_at',
            'updated_at',
        ],
    )
