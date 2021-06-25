from binance.spot import Spot as BinanceClient
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import time

#thingsboard mqtt host.
#Ensure port 1883 is not blocked by your firewall
TB_MQTT_HOST = "mqtt.example.com"

#thingsboard device access token
TB_DEVICE_KEY = "DEVICE-ACESS-TOKEN"
device = TBDeviceMqttClient(TB_MQTT_HOST, TB_DEVICE_KEY)

#Binance client

#Using testing API
binance_client = BinanceClient(base_url="https://testnet.binance.vision")

#Using your account:
#Ensure API is enabled.
#binance_client = BinanceClient(key="YOUR-BINANCE-KEY", secret="YOUR-BINANCE-SECRET"))

#Get latest price
def getPrice(trade):

    try:
        response = binance_client.ticker_price(trade)
        price = response.get('price')
        print(price)
        return price

    except Exception as e:
        print(e)
        return None


def sendTb(timeseries):
    device.connect()
    result = device.send_telemetry(timeseries)
    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS #wait to receive result
    device.disconnect()

while True:

    try:

        #trade to follow Bitcoin / USDT
        trade = "BTCUSDT"

        #get price from Binance
        price = getPrice(trade)

        if price != None:
            #prepare timeseries
            timeseries = {
                trade: price
            }

            #send to Thingsboard
            sendTb(timeseries)

    except Exception as e:
        print(e)

    time.sleep(15) #wait 15seconds
