import os
import random
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(receiver_email, otp):

    message = EmailMessage()

    message["Subject"] = "Password Reset OTP - Library Management System "
    message["From"] = f"Library Management System <{SMTP_EMAIL}>"
    message["To"] = receiver_email

    message.set_content(
        f"""
Hello,

Your OTP for resetting your Library Management System password is:

{otp}

This OTP is valid for 5 minutes only.

If you did not request a password reset, please ignore this email.

Regards,
Library Management System
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.send_message(message)