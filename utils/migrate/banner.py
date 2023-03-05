import os
import datetime
import mysql.connector

from banner.models import Banner

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, big_title, small_title, sort, image, created_at, updated_at from banners"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    big_title = row[1]
    small_title = row[2]
    sort = row[3]
    image = row[4]
    created_at = row[5]
    updated_at = row[6]

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    banner_obj = Banner.objects.create(
        id=id,
        big_title=big_title,
        small_title=small_title,
        sort=sort,
        image=image,
        created_at=created_at,
        updated_at=updated_at,
    )
