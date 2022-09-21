import smtplib
import datetime as dt
import random
import pandas as pd

MY_EMAIL = "YOUR_EMAIL@gmail.com"
PASSWORD = "YOUR_PASSWORD"
LETTERS = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]

# Get the actual date
now = dt.datetime.now()
month = now.month
day = now.day

# DataFrame of birthdays
birthdays = pd.read_csv("birthdays.csv")

# Write letter
for row in birthdays.itertuples(index=False):
    if row.month == month and row.day == day:
        # Choose a random letter
        letter = random.choice(LETTERS)
        with open(f"letter_templates/{letter}", 'r') as letter_template:
            letter_list = letter_template.readlines()
        with open(f"letter_output/letter_for_{row.name}", 'w') as my_letter:
            for line in letter_list:
                replaced_letter_name = line.replace("[NAME]", row.name)
                birthday_letter = my_letter.write(replaced_letter_name)
        # Send letter
        with open(f"letter_output/letter_for_{row.name}", 'r') as letter_to_send:
            content = letter_to_send.read()
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=row.email,
                msg=f"Subject:Happy Birthday!!!\n\n{content}"
            )
