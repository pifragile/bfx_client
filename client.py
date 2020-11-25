import asyncio
import time
import utils
from bfxapi import Client as BfxClient
from settings import *
from statistics import mean
from twilio.rest import Client as TwilioClient

bfx = BfxClient(
    API_KEY=API_KEY,
    API_SECRET=API_SECRET,
    logLevel='WARNING',
    max_retries=10000
)

twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@bfx.ws.on('authenticated')
async def subscribe(self):
    await bfx.ws.unsubscribe_all()
    await bfx.ws.subscribe_trades(PAIR_SYMBOL)
    await bfx.ws.subscribe_order_book(PAIR_SYMBOL)
    await bfx.ws.subscribe_candles(PAIR_SYMBOL, f'{CANDLE_TIME_FRAME}m')
    if ALERTS_ACTIVE:
        asyncio.ensure_future(alert_on_fast_price_increase())


@bfx.ws.on('new_trade')
async def monitor(self):
    if MONITORING_ACTIVE:
        try:
            orders = await bfx.rest.get_active_orders(PAIR_SYMBOL)
            ticker = await bfx.rest.get_public_ticker(PAIR_SYMBOL)
            os.system('clear')
            print(f'bid: {ticker[0]} ask: {ticker[2]}')
            for order in orders:
                side = 'buy' if order.amount > 0 else 'sell'
                mts_create = order.mts_create
                age_string = utils.ms_to_age_string(time.time() * 1000 - mts_create)
                print(f'{side} at {order.price}, age: {age_string}')
        except Exception:
            pass


def send_twilio_test_message(message1, message2):
    message = 'Your {} code is {}'.format(message1, message2)
    twilio_client.messages.create(
        from_=f'whatsapp:{TWILIO_FROM_NUMBER}',
        body=message,
        to=f'whatsapp:{WHATSAPP_TO_NUMBER}'
    )


def calculate_gradient_weight_function(x):
    a = CANDLE_GRADIENT_WEIGHT_FUNCTION_A
    b = CANDLE_GRADIENT_WEIGHT_FUNCTION_B
    return (a * x + b) / 100


async def alert_on_fast_price_increase():
    while True:
        candles = await bfx.rest.get_public_candles(PAIR_SYMBOL, None, None, tf=f'{CANDLE_TIME_FRAME}m',
                                                    limit=f'{CANDLE_LOOK_BACK}')
        # candle format: [mts, open_price, close_price, high, low, volume]
        price_increases = [candle[2] / candle[1] - 1 for candle in candles]
        price_gradients = []

        # calculate the average price increase for the last i candles
        for i, _ in enumerate(price_increases):
            price_gradients.append(mean(price_increases[:i + 1]))

        last_candle = price_gradients[0]
        for i, price_gradient in enumerate(price_gradients):
            threshold = calculate_gradient_weight_function(i)

            if price_gradient > threshold and last_candle > LATEST_CANDLE_MINIMUM / 100:
                send_twilio_test_message(f'last {i + 1} candles are up {round(price_gradient * 100, 2)}%', '🥳')
                break
        time.sleep(CANDLE_TIME_FRAME * 60)


@bfx.ws.on('error')
async def restart(self):
    bfx.ws.run()


bfx.ws.run()
send_twilio_test_message(f'app started', '🥳')
