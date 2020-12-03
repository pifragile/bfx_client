import asyncio
import datetime
import time
from statistics import mean

from bfxapi import Client as BfxClient

from settings import *
from utils import misc_utils

bfx = BfxClient(
    API_KEY=BFX_API_KEY,
    API_SECRET=BFX_API_SECRET,
    logLevel='ERROR',
    max_retries=10000
)

latest_candle_processed = None


def send_alert_email(subject, message):
    misc_utils.send_email(subject, message, EMAIL_RECEIVER, 'bfx alert')


async def alert_on_fast_price_increase():
    global latest_candle_processed
    if ALERTS_ACTIVE:
        while True:
            try:
                candles = await bfx.rest.get_public_candles(PAIR_SYMBOL, None, None, tf=f'{CANDLE_TIME_FRAME}m',
                                                            limit=f'{CANDLE_LOOK_BACK + 1}')
            except Exception as e:
                print(e)
                time.sleep(10)
                continue

            candles = candles[1:]
            if candles[0] != latest_candle_processed:
                latest_candle_processed = candles[0]
                # candle format: [mts, open_price, close_price, high, low, volume]
                price_increases = [candle[2] / candle[1] - 1 for candle in candles]
                price_gradients = []
                print(f'{datetime.datetime.now()}: {price_increases}')
                # calculate the average price increase for the last i candles
                for i, _ in enumerate(price_increases):
                    price_gradients.append(mean(price_increases[:i + 1]))

                last_candle = price_gradients[0]
                for i, price_gradient in enumerate(price_gradients):
                    threshold = misc_utils.calculate_gradient_weight_function(i)

                    if price_gradient > threshold and last_candle > LATEST_CANDLE_MINIMUM / 100:
                        alert_string = f'last {i + 1} candles are up {round(price_gradient * 100, 2)}% 🥳'
                        send_alert_email(alert_string, alert_string)
                        break
            time.sleep(10)


send_alert_email('app starting', 'app starting')
asyncio.run(alert_on_fast_price_increase())
