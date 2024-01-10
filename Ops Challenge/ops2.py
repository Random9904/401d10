import time
from ping3 import ping
import smtplib
from email.mime.text import MIMEText
import keyring
from getpass import getpass

# Send an email to the administrator if a host status changes (from “up” to “down” or “down” to “up”)
# Clearly indicate in the message which host status changed, the status before and after, and a timestamp of the event.
def send_notification(email, password, host, previous_status, current_status, admin_email):
    subject = f"Host Status Change - {host}"
    body = f"Host: {host}\nPrevious Status: {previous_status}\nCurrent Status: {current_status}\nTimestamp: {time.ctime()}"

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = email
    message["To"] = admin_email

    # |--------------------------------Change server here ---------------------------------------|
    with smtplib.SMTP("EXAMPLE.SMTP.SERVER", 587) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message.as_string())

# Transmit a single ICMP (ping) packet to a specific IP every two seconds
# Target address
destination_ip = "192.168.1.1"
# Number of seconds
interval = 2
# Ask the user for an email address and password to use for sending notifications
user_email = input("Enter your email address: ")
user_password = getpass("Enter your email password: ")
admin_email = input("Enter admin email address: ")

APP_NAME = "yeye"
keyring.set_password(APP_NAME, user_email, user_password)

# Send an email to the administrator if a host status changes (from “up” to “down” or “down” to “up”)
host = "example.com"
previous_status = "up"
current_status = "up"

# Only run while True meaning forever
while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    response = ping(destination_ip)
    # Set the value of success while not NULL
    success = response is not None
    # Evaluate the response as either success or failure
    # Assign success or failure to a status variable
    status = "Success" if success else "Failure"
    # For every ICMP transmission attempted, print the status variable along 
    # with a comprehensive timestamp and destination IP tested
    print(f"{timestamp} - Destination: {destination_ip} - Status: {status}")

    time.sleep(interval)

    # NEW CODE
    time.sleep(5)
    current_status = "down" if current_status == "up" else "up"

    if previous_status != current_status:
        stored_password = keyring.get_password(APP_NAME, user_email)
        # Send an email to the administrator if a host status changes (from “up” to “down” or “down” to “up”)
        send_notification(user_email, stored_password, host, previous_status, current_status, admin_email)
        previous_status = current_status