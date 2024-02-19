from smtplib import SMTP
from email.message import EmailMessage


def send_email(name, email, phone, message):
    your_email = "Your email"
    your_password = "Your password"
    content = f"Name: {name}\n" \
              f"Email: {email}\n" \
              f"Phone: {phone}\n" \
              f"Message:{message}"
    msg = EmailMessage()
    msg["Subject"] = f"New message from {name}"
    msg["From"] = your_email
    msg["To"] = your_email
    msg.set_content(content)
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(your_email, your_password)
        connection.send_message(msg)
