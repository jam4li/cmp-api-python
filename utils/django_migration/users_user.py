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

cmd = "select id, email, name, enable_google_2fa_verification, google_2fa_secret, created_at, updated_at, first_name, last_name, date_joined from users_user"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    email = row[1]
    name = row[2]
    enable_google_2fa_verification = row[3]
    google_2fa_secret = row[4]
    created_at = row[5]
    updated_at = row[6]
    first_name = row[7]
    last_name = row[8]
    date_joined = row[9]

    # Check enable_google_2fa_verification to set True or False
    if enable_google_2fa_verification == 0:
        enable_google_2fa_verification = False
    else:
        enable_google_2fa_verification = True

    try:
        user_obj = User.objects.get(id=id)
    except User.DoesNotExist:
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = User(id=id, email=email)

    user_obj.email = email
    user_obj.name = name
    user_obj.enable_google_2fa_verification = enable_google_2fa_verification
    user_obj.google_2fa_secret = google_2fa_secret
    user_obj.created_at = created_at
    user_obj.updated_at = updated_at
    user_obj.save()
