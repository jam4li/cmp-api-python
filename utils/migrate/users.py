import os
import datetime
import mysql.connector

from apps.users.models import User, UserProfile

from apps.package.models import Package

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, package_id, referrer_id, email, ex_email, username, referrer_code, status, enable_google_2fa_verification, google_2fa_secret, name, avatar, role, trc20_withdraw_wallet, weekly_withdraw_amount, weekly_withdraw_date, created_at, updated_at from users"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    package_id = row[1]
    referrer_id = row[2]
    email = row[3]
    ex_email = row[4]
    username = row[5]
    referrer_code = row[6]
    status = row[7]
    enable_google_2fa_verification = row[8]
    google_2fa_secret = row[9]
    name = row[10]
    avatar = row[11]
    role = row[12]
    trc20_withdraw_wallet = row[13]
    weekly_withdraw_amount = row[14]
    weekly_withdraw_date = row[15]
    created_at = row[16]
    updated_at = row[17]

    # Find Package and User
    try:
        package = Package.objects.get(id=package_id)
    except Package.DoesNotExist:
        package = None

    try:
        referrer_user = User.objects.get(id=referrer_id)
        referrer = UserProfile.objects.get(user=referrer_user)
    except User.DoesNotExist:
        referrer = None

    # Check status to set True or False
    if status == 0:
        status = False
    else:
        status = True

    # Check enable_google_2fa_verification to set True or False
    if enable_google_2fa_verification == 0:
        enable_google_2fa_verification = False
    else:
        enable_google_2fa_verification = True

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if weekly_withdraw_date:
        weekly_withdraw_date = datetime.datetime.strptime(
            str(weekly_withdraw_date),
            date_format,
        )

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    user_obj = User.objects.create(
        id=id,
        email=email,
        name=name,
        enable_google_2fa_verification=enable_google_2fa_verification,
        google_2fa_secret=google_2fa_secret,
        created_at=created_at,
        updated_at=updated_at,
    )

    user_profile = UserProfile.objects.create(
        user=user_obj,
        username=username,
        package=package,
        referrer=referrer,
        ex_email=ex_email,
        referrer_code=referrer_code,
        status=status,
        avatar=avatar,
        role=role,
        trc20_withdraw_wallet=trc20_withdraw_wallet,
        weekly_withdraw_amount=weekly_withdraw_amount,
        weekly_withdraw_date=weekly_withdraw_date,
    )
