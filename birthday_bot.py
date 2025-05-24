import pandas as pd
from datetime import datetime
from twilio.rest import Client
import schedule
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Twilio credentials from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)

def send_birthday_message(to, name):
    message = f"🎉 Happy Birthday, {name}! 🎂🎈 Have a wonderful day!"
    message = client.messages.create(
        body=message,
        from_=twilio_whatsapp_number,
        to=to
    )
    print(f"Sent message to {name} ({to}): SID {message.sid}")

def check_and_send_birthday_wishes():
    print(f"Checking birthdays on {datetime.now().strftime('%Y-%m-%d')}...")
    df = pd.read_csv("birthday.csv")

    today = datetime.now().strftime("%m-%d")
    birthday_people = df[df['birthday'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%m-%d") == today)]

    for _, person in birthday_people.iterrows():
        send_birthday_message(person['phone'], person['name'])

# Schedule to run every day at 4:30 PM
schedule.every().day.at("12:20").do(check_and_send_birthday_wishes)

if __name__ == "__main__":
    print("WhatsApp Birthday Bot started... Will send messages at 4:55 PM daily.")
    while True:
        schedule.run_pending()
        time.sleep(60)
