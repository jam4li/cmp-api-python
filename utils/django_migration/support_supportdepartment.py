import os
import mysql.connector

from apps.support.models import SupportDepartment

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP_DJANGO'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, name, icon, is_active, created_at, updated_at from support_supportdepartment"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    name = row[1]
    icon = row[2]
    is_active = row[3]
    created_at = row[4]
    updated_at = row[5]

    if is_active == 0:
        is_active = False
    else:
        is_active = True

    support_department_obj = SupportDepartment.objects.create(
        id=id,
        name=name,
        icon=icon,
        is_active=is_active,
        created_at=created_at,
        updated_at=updated_at,
    )
