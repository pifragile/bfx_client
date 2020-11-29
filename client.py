import datetime
import time
from statistics import mean

from bfxapi import Client as BfxClient

from settings import *
from utils import datetime_utils, misc_utils

bfx = BfxClient(
    API_KEY=BFX_API_KEY,
    API_SECRET=BFX_API_SECRET,
    logLevel='ERROR',
    max_retries=10000
)

latest_candle_processed = None

@bfx.ws.on('authenticated')
async def subscribe(self):
    await bfx.ws.unsubscribe_all()
    await bfx.ws.subscribe_trades(PAIR_SYMBOL)
    await bfx.ws.subscribe_order_book(PAIR_SYMBOL)
    await bfx.ws.subscribe_candles(PAIR_SYMBOL, f'{CANDLE_TIME_FRAME}m')


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
                age_string = datetime_utils.ms_to_age_string(time.time() * 1000 - mts_create)
                print(f'{side} at {order.price}, age: {age_string}')
        except Exception:
            pass


@bfx.ws.on('new_trade')
async def alert_on_fast_price_increase(trade):
    global latest_candle_processed
    if ALERTS_ACTIVE:
        candles = await bfx.rest.get_public_candles(PAIR_SYMBOL, None, None, tf=f'{CANDLE_TIME_FRAME}m',
                                                    limit=f'{CANDLE_LOOK_BACK + 1}')

        candles = candles[1:]
        if candles[0] == latest_candle_processed:
            return
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
                misc_utils.send_twilio_test_message(f'last {i + 1} candles are up {round(price_gradient * 100, 2)}%',
                                                    '🥳')
                break


@bfx.ws.on('error')
async def restart(self):
    bfx.ws.run()


bfx.ws.run()
misc_utils.send_twilio_test_message(f'app started', '🥳')
