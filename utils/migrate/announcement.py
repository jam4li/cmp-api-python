import os
import datetime
import mysql.connector

from apps.announcement.models import Announcement

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, title, author, image, status, summery, text, publish_date, created_at, updated_at from announcements"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    title = row[1]
    author = row[2]
    image = row[3]
    status = row[4]
    summary = row[5]
    text = row[6]
    publish_date = row[7]
    created_at = row[8]
    updated_at = row[9]

    # Change mysql's date to python's date
    date_format = '%Y-%m-%d %H:%M:%S'

    if created_at:
        created_at = datetime.datetime.strptime(str(created_at), date_format)

    if updated_at:
        updated_at = datetime.datetime.strptime(str(updated_at), date_format)

    if publish_date:
        publish_date = datetime.datetime.strptime(
            str(publish_date),
            date_format,
        )

    announcement_obj = Announcement.objects.create(
        id=id,
        title=title,
        author=author,
        image=image,
        status=status,
        summary=summary,
        text=text,
        publish_date=publish_date,
        created_at=created_at,
        updated_at=updated_at,
    )
