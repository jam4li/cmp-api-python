import os
import datetime
import mysql.connector

from apps.banner.models import Banner

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

    banner_obj = Banner.objects.create(
        id=id,
        big_title=big_title,
        small_title=small_title,
        sort=sort,
        image=image,
        created_at=created_at,
        updated_at=updated_at,
    )
