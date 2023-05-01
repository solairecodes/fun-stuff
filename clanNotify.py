import requests
import time
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your Bungie API key and clan ID
api_key = os.environ.get("API_KEY")
clan_id = os.environ.get("CLAN_ID")

# Set your email information
sender_email = os.environ.get("SENDER_EMAIL")
recipient_email = os.environ.get("RECIPIENT_EMAIL")
sender_password = os.environ.get("SENDER_PASSWORD")

# Set the time interval for checking the clan roster (in seconds)
check_interval = 300

# Set the URL for the Bungie API endpoint
base_url = "https://www.bungie.net/Platform"
headers = {"X-API-Key": api_key}

# Function to send an email notification
def send_email_notification(member_name):
    message = f"{member_name} has left the clan."
    msg = MIMEText(message)
    msg['Subject'] = "Clan Member Left Notification"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

# Main loop to check the clan roster
while True:
    try:
        # Get the current clan roster
        response = requests.get(f"{base_url}/GroupV2/{clan_id}/Members/", headers=headers)
        response_data = response.json()['Response']['results']

        # Check if any members have left the clan
        for member in response_data:
            if member['membershipType'] == 3 and not member['isMember']:
                member_name = member['destinyUserInfo']['displayName']
                send_email_notification(member_name)

        # Wait for the specified time interval before checking again
        time.sleep(check_interval)

    except Exception as e:
        print(e)
