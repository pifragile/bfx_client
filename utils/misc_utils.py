import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from twilio.rest import Client as TwilioClient

import settings

twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_twilio_test_message(message1, message2):
    message = 'Your {} code is {}'.format(message1, message2)
    twilio_client.messages.create(
        from_=f'whatsapp:{settings.TWILIO_FROM_NUMBER}',
        body=message,
        to=f'whatsapp:{settings.WHATSAPP_TO_NUMBER}'
    )


def calculate_gradient_weight_function(x):
    a = settings.CANDLE_GRADIENT_WEIGHT_FUNCTION_A
    b = settings.CANDLE_GRADIENT_WEIGHT_FUNCTION_B
    return (a * x + b) / 100


def send_email(subject, msg, to, from_name):
    smtp_server = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    sender_email = settings.EMAIL_USER
    password = settings.EMAIL_PASSWORD

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f'{from_name}<{settings.EMAIL_USER}>'
        message["To"] = to
        message.attach(MIMEText(msg, "plain"))
        server.sendmail(sender_email, to, message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()


__all__ = ['send_twilio_test_message', 'calculate_gradient_weight_function']
