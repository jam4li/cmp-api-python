import os
import mysql.connector

from apps.exchange.models import ExchangeParent
from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, parent_id, status, user_id, created_at, updated_at from exchange_exchangeparent"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    parent_id = row[1]
    status = row[2]
    user_id = row[3]
    created_at = row[4]
    updated_at = row[5]

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    try:
        parent = ExchangeParent.objects.get(id=parent_id)
    except:
        parent = None

    exchange_obj = ExchangeParent.objects.create(
        id=id,
        parent=parent,
        status=status,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
