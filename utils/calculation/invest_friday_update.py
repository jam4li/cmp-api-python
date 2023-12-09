# This script appears to be focused on updating the updated_at field in the "invests" table for certain records.
# The primary goal is to ensure that records with an updated_at value falling on a Saturday or Sunday are modified
# to have an updated_at value corresponding to the previous Friday.
# This adjustment is made to facilitate the accurate calculation of profits added to the "invests" table
# on Mondays for each user.

import os
import decimal
import mysql.connector
from datetime import datetime, timedelta

host = 'localhost'
database = 'cloudminepro'
user = 'root'
password = '}86{NY[*<uXEB3'

# Create a connection to the database
mydb = mysql.connector.connect(
    host=host,
    database=database,
    user=user,
    password=password,
)

mycursor = mydb.cursor()

query = "SELECT id, updated_at from invests where finished=0 AND DATE(updated_at)<'2023-06-01'"

mycursor.execute(query)

myresult = mycursor.fetchall()


def is_weekend(date):
    if date.weekday() >= 5:  # 5 and 6 correspond to Saturday and Sunday
        return True
    return False


for invest in myresult:
    invest_id = invest[0]
    invest_date = invest[1].date()

    if is_weekend(invest_date):
        print(str(invest))

        previous_friday = invest_date - timedelta(
            days=(invest_date.weekday() + 3) % 7,
        )

        update_invest_query = "UPDATE invests set updated_at='{0}' where id='{1}'".format(
            previous_friday,
            invest_id,
        )

        mycursor.execute(update_invest_query)
        mydb.commit()

        print(update_invest_query)
