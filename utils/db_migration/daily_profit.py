import os
import datetime
import mysql.connector

from config.models import DailyProfit

mydb = mysql.connector.connect(
    port=3306,
    host=os.getenv('DATABASE_HOST_BACKUP'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME'),
)

cursor = mydb.cursor()

cmd = "select id, daily_profit, created_at, updated_at from daily_profits"

cursor.execute(cmd)

records = cursor.fetchall()

for row in records:
    id = row[0]
    daily_profit = row[1]
    created_at = row[2]
    updated_at = row[3]

    daily_profit_obj = DailyProfit.objects.create(
        id=id,
        daily_profit=daily_profit,
        created_at=created_at,
        updated_at=updated_at,
    )
