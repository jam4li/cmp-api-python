import os
import datetime
import mysql.connector
import pytz
import decimal

from apps.users.models import User
from apps.network.models import NetworkTransaction
from apps.invest.models import Invest

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

cmd = "select id, user_id, invest_id, type, amount, day, description, created_at, updated_at, deleted_at from network_transactions"

cursor.execute(cmd)

new_objects = []

batch_size = 2500
fetch_counter = 0

while True:
    records = cursor.fetchmany(batch_size)

    fetch_counter += batch_size
    print(fetch_counter)

    if not records:
        break

    for row in records:
        id = row[0]

        try:
            network_transaction_obj = NetworkTransaction.objects.get(id=id)
            continue

        except NetworkTransaction.DoesNotExist:
            network_transaction_obj = NetworkTransaction(id=id)

        user_id = row[1]
        invest_id = row[2]
        type = row[3]
        amount = row[4]
        day = row[5]
        description = row[6]
        created_at = row[7]
        updated_at = row[8]
        deleted_at = row[9]

        user_ids.add(user_id)
        invest_ids.add(invest_id)

        network_transaction_obj.type = type
        network_transaction_obj.amount = amount
        network_transaction_obj.day = day
        network_transaction_obj.description = description
        network_transaction_obj.created_at = created_at
        network_transaction_obj.updated_at = updated_at
        network_transaction_obj.deleted_at = deleted_at

        new_objects.append(network_transaction_obj)

    if len(new_objects) > 5000:
        users = User.objects.filter(
            id__in=user_ids
        ).prefetch_related('user')

        invests = Invest.objects.filter(
            id__in=invest_ids
        ).prefetch_related('invest')

        # Create dictionaries for efficient lookup
        user_dict = {user.id: user for user in users}
        invest_dict = {invest.id: invest for invest in invests}

        for i in range(len(new_objects) - 1, -1, -1):
            obj = new_objects[i]
            user_id = obj.user_id
            invest_id = obj.invest_id

            if user_id in user_dict and invest_id in invest_dict:
                obj.user = user_dict[user_id]
                obj.invest = invest_dict[invest_id]

            else:
                del new_objects[i]

        NetworkTransaction.objects.bulk_create(new_objects)

        new_objects = []
        user_ids = set()
        invest_ids = set()


if new_objects:
    # Fetch related objects for the remaining new_objects
    users = User.objects.filter(
        id__in=user_ids
    ).prefetch_related('user')
    invests = Invest.objects.filter(
        id__in=invest_ids
    ).prefetch_related('invest')

    # Create dictionaries for efficient lookup
    user_dict = {user.id: user for user in users}
    invest_dict = {invest.id: invest for invest in invests}

    # Update the user and invest fields of the new_objects
    for obj in new_objects:
        user_id = obj.user_id
        invest_id = obj.invest_id
        obj.user = user_dict.get(user_id)
        obj.invest = invest_dict.get(invest_id)

    # Perform bulk create for the remaining new_objects
    NetworkTransaction.objects.bulk_create(new_objects)
