import os
import mysql.connector
import decimal
from datetime import datetime, date, timedelta

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

start_date = date(2023, 1, 1)
end_date = date(2023, 6, 1)

# Define a function to check if a given date is a Saturday or Sunday


def is_weekend(date):
    return date.weekday() in [5, 6]  # Saturday (5) or Sunday (6)


# Generate the list of dates excluding weekends
dates = []
current_date = start_date
while current_date <= end_date:
    if not is_weekend(current_date):
        dates.append(current_date)
    current_date += timedelta(days=1)

# Print the list of dates
for index, date in enumerate(dates):
    try:
        current_date = date

        next_date = dates[index+1]
        next_date = str(next_date) + " 00:00:00"
        next_date = datetime.strptime(next_date, '%Y-%m-%d %H:%M:%S')
        next_date = next_date.strftime('%Y-%m-%d %H:%M:%S')

    except IndexError:
        print("An IndexError occurred. Index out of range.")
        continue

    query = "SELECT id, user_id, invest, profit from invests where finished=0 AND DATE(updated_at)='{0}'".format(
        current_date,
    )

    mycursor.execute(query)
    myresult = mycursor.fetchall()

    for invest in myresult:
        invest_id = invest[0]
        invest_user_id = invest[1]
        invest_invest = invest[2]
        invest_profit = invest[3]

        # Calculate new profit
        daily_percent = decimal.Decimal(0.27)
        new_profit = (daily_percent * invest_invest) / 100

        invest_profit += new_profit

        update_invest_query = "UPDATE invests set profit={0}, calculated_at='{1}', updated_at='{1}' where id={2}".format(
            invest_profit,
            next_date,
            invest_id,
        )

        mycursor.execute(update_invest_query)
        mydb.commit()

        print(update_invest_query)

        network_transactions_description = "daily profit of {0}$".format(
            invest_invest,
        )

        update_network_transactions_query = "INSERT INTO network_transactions (user_id, invest_id, type, amount, day, description, created_at) VALUES ({0}, {1}, '{2}', {3}, {4}, '{5}', '{6}')".format(
            invest_user_id,
            invest_id,
            'profit',
            new_profit,
            1,
            network_transactions_description,
            next_date,
        )

        mycursor.execute(update_network_transactions_query)
        mydb.commit()

        print(update_network_transactions_query)

        # Get profit wallet
        all_user_wallet_query = "SELECT user_id, wallet_id from user_wallet where user_id={0}".format(
            invest_user_id,
        )
        mycursor.execute(all_user_wallet_query)
        all_user_wallet = mycursor.fetchall()

        for user_wallet in all_user_wallet:
            user_wallet_id = user_wallet[1]

            wallet_query = "SELECT type, balance from wallets where id={0}".format(
                user_wallet_id,
            )
            mycursor.execute(wallet_query)
            wallet_result = mycursor.fetchone()

            if wallet_result[0] == 'profit':
                new_wallet_profit_balance = wallet_result[1] + new_profit

                update_wallet_query = "UPDATE wallets set balance={0}, updated_at='{1}' where id={2}".format(
                    new_wallet_profit_balance,
                    next_date,
                    user_wallet_id,
                )
                mycursor.execute(update_wallet_query)
                mydb.commit()

                print(update_wallet_query)
