import os
import datetime
import mysql.connector
import decimal

from apps.referral.models import Referral

from apps.users.models import User
from apps.network.models import Network

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, user_id, network_id, referrer_id, recruited, binary_place, created_at, updated_at from referrals"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    user_id = row[1]
    network_id = row[2]
    referrer_id = row[3]
    recruited = row[4]
    binary_place = row[5]
    created_at = row[6]
    updated_at = row[7]

    # Find User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        pass

    # Find Network
    try:
        network = Network.objects.get(id=network_id)
    except Network.DoesNotExist:
        pass

    # Find Referrer
    try:
        referrer = User.objects.get(id=referrer_id)
    except User.DoesNotExist:
        referrer = None

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    referral_obj = Referral.objects.create(
        id=id,
        user=user,
        network=network,
        referrer=referrer,
        recruited=recruited,
        binary_place=binary_place,
        created_at=created_at,
        updated_at=updated_at,
    )
