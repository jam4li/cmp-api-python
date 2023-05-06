import os
import mysql.connector

from apps.support.models import SupportDepartment, SupportTicket
from apps.users.models import User

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, title, content, attachments, important_level, status, department_id, user_id, created_at, updated_at from support_supportticket"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    title = row[1]
    content = row[2]
    attachments = row[3]
    important_level = row[4]
    status = row[5]
    department_id = row[6]
    user_id = row[7]
    created_at = row[8]
    updated_at = row[9]

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        continue

    try:
        department = SupportDepartment.objects.get(id=department_id)
    except SupportDepartment.DoesNotExist:
        continue

    support_ticket_obj = SupportTicket.objects.create(
        id=id,
        title=title,
        content=content,
        attachments=attachments,
        important_level=important_level,
        status=status,
        department=department,
        user=user,
        created_at=created_at,
        updated_at=updated_at,
    )
