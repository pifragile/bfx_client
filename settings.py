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

# list that indicates the price increases of latest candles necessary to trigger an alert
# eg. l=[0.006,0.005] triggers alert when last candle is up 0.6% or when last 2 candles are up 0.5% on average
CANDLE_GRADIENT_THRESHOLDS = [float(x) for x in os.getenv('CANDLE_GRADIENT_THRESHOLDS').split(',')]
CANDLE_GRADIENT_THRESHOLDS_DEFAULT = os.getenv('CANDLE_GRADIENT_THRESHOLDS_DEFAULT')

# email
EMAIL_HOST = 'send.one.com'
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
