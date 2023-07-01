import os
import datetime
import mysql.connector
import decimal
import pytz

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

cursor.execute("SET GLOBAL wait_timeout = 28800")
cursor.execute("SET GLOBAL interactive_timeout = 28800")
cursor.execute("SET SESSION net_read_timeout=28800")
cursor.execute("SET SESSION net_write_timeout=28800")

cmd = "select id, user_id, network_id, referrer_id, recruited, binary_place, created_at, updated_at from referrals"

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
        network_id = row[2]
        referrer_id = row[3]
        recruited = row[4]
        binary_place = row[5]
        created_at = row[6]
        updated_at = row[7]

        # Find User
        try:
            user = User.objects.get(id=user_id)
            network = Network.objects.get(id=network_id)
        except User.DoesNotExist:
            pass
        except Network.DoesNotExist:
            pass

        try:
            referrer = User.objects.get(id=referrer_id)
        except User.DoesNotExist:
            referrer = None

        if created_at is None:
            created_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        if updated_at is None:
            updated_at = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

        try:
            referral_obj = Referral.objects.get(id=id)
        except Referral.DoesNotExist:
            referral_obj = Referral(id=id)
            new_objects.append(referral_obj)

        referral_obj.user = user
        referral_obj.network = network
        referral_obj.referrer = referrer
        referral_obj.recruited = recruited
        referral_obj.binary_place = binary_place
        referral_obj.created_at = created_at
        referral_obj.updated_at = updated_at

        existing_objects.append(referral_obj)

    if len(new_objects) > 5000:
        Referral.objects.bulk_create(new_objects)
        new_objects = []

    if len(existing_objects) > 5000:
        Referral.objects.bulk_update(
            existing_objects, [
                'user',
                'network',
                'referrer',
                'recruited',
                'binary_place',
                'created_at',
                'updated_at',
            ],
        )
        existing_objects = []


if new_objects:
    Referral.objects.bulk_create(new_objects)

if existing_objects:
    Referral.objects.bulk_update(
        existing_objects,
        [
            'user',
            'network',
            'referrer',
            'recruited',
            'binary_place',
            'created_at',
            'updated_at',
        ],
    )
