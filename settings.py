import os

from dotenv import load_dotenv

load_dotenv()
BFX_API_KEY = os.getenv('BFX_API_KEY')
BFX_API_SECRET = os.getenv('BFX_API_SECRET')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
WHATSAPP_TO_NUMBER = os.getenv('WHATSAPP_TO_NUMBER')

MONITORING_ACTIVE = os.getenv('MONITORING_ACTIVE', 'False') == 'True'
ALERTS_ACTIVE = os.getenv('ALERTS_ACTIVE', 'False') == 'True'

PAIR_SYMBOL = 'tBTCUSD'

CANDLE_TIME_FRAME = 5  # minutes
# number of candles in the to consider for fast price increase alerts
CANDLE_LOOK_BACK = 5
# minimum price increase in % of the latest candle necessary to trigger an alert
# used to prevent alerts for increases in the past
LATEST_CANDLE_MINIMUM = 0.1

# parameters of a linear function f(x) = ax+b, where f(#candles in the past) determines the average price increase
# of each candle necessary to trigger an alert
# example: a=-0.1 b=0.7, so f(0)=0.7 and f(1)=0.5
# so if the last candle had a price increase of more than 0.7% OR the last 2 candles had more than an average price
# increase of more than 0.5% an alert will be triggered
CANDLE_GRADIENT_WEIGHT_FUNCTION_A = -0.085
CANDLE_GRADIENT_WEIGHT_FUNCTION_B = 0.7
