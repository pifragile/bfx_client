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


__all__ = ['send_twilio_test_message', 'calculate_gradient_weight_function']
