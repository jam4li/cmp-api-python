import os
import mysql.connector
from django.utils import timezone

from apps.users.models import User, UserProfile

from apps.package.models import Package

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, username, ex_email, referrer_code, status, avatar, role, trc20_withdraw_wallet, weekly_withdraw_amount, weekly_withdraw_date, package_id, referrer_id, user_id from users_userprofile"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    username = row[1]
    ex_email = row[2]
    referrer_code = row[3]
    status = row[4]
    avatar = row[5]
    role = row[6]
    trc20_withdraw_wallet = row[7]
    weekly_withdraw_amount = row[8]
    weekly_withdraw_date = row[9]
    package_id = row[10]
    referrer_id = row[11]
    user_id = row[12]

    if status == 0:
        status = False
    else:
        status = True

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        package = None

    try:
        referrer = UserProfile.objects.get(id=referrer_id)
    except UserProfile.DoesNotExist:
        referrer = None

    package_obj = UserProfile.objects.create(
        id=id,
        username=username,
        ex_email=ex_email,
        referrer_code=referrer_code,
        status=status,
        avatar=avatar,
        role=role,
        trc20_withdraw_wallet=trc20_withdraw_wallet,
        weekly_withdraw_amount=weekly_withdraw_amount,
        weekly_withdraw_date=weekly_withdraw_date,
        package=package,
        referrer=referrer,
        user=user,
    )
