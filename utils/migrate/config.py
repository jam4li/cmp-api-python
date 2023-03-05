import os
import datetime
import mysql.connector

from config.models import Config

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, `key`, value, created_at, updated_at from configs"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    key = row[1]
    value = row[2]
    created_at = row[3]
    updated_at = row[4]

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    config_obj = Config.objects.create(
        id=id,
        key=key,
        value=value,
        created_at=created_at,
        updated_at=updated_at,
    )
