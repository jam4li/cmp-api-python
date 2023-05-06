import os
import mysql.connector

from apps.referral.models import Referral
from apps.users.models import User
from apps.network.models import Network

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, recruited, binary_place, network_id, referrer_id, user_id, created_at, updated_at from referrals"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    recruited = row[1]
    binary_place = row[2]
    network_id = row[3]
    referrer_id = row[4]
    user_id = row[5]
    created_at = row[6]
    updated_at = row[7]

    try:
        network = Network.objects.get(id=network_id)
    except:
        continue

    try:
        user = User.objects.get(id=user_id)
    except:
        continue

    try:
        referrer = User.objects.get(id=referrer_id)
    except:
        referrer = None

    referral_obj = Referral.objects.create(
        id=id,
        recruited=recruited,
        binary_place=binary_place,
        network=network,
        referrer=referrer,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
