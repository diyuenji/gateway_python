import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_IDS = ["LED","FAN", "LCD","Fan control"]
AIO_USERNAME = "diyuenji"
AIO_KEY ="aio_LElr62VGWmZdcsJuw4z5denwtDmU"

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subcribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if isYolobitConnected:
        ser.write(str(payload).encode("utf-8"))

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB-SERIAL CH340" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

isYolobitConnected = False
if getPort() != "None":
    ser = serial.Serial( port=getPort(), baudrate=115200)
    isYolobitConnected = True


def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    try:
        if splitData[0] == "TEMP":
            client.publish("do-an.temp", splitData[1])
        if splitData[0] == "LED":
            client.publish("do-an.led", splitData[1])
        if splitData[0] == "FAN":
            client.publish("do-an.fan", splitData[1])
        if splitData[0] == "LCD":
            client.publish("do-an.lcd", splitData[1])
        if splitData[0] == "FANC":
            client.publish("do-an.fan-control", splitData[1])    
    except:
        pass


mess = ""
def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

while True:
    if isYolobitConnected:
        readSerial()
    # client.publish("diyuenji/feeds/do-an.temp", 10)
    time.sleep(1)