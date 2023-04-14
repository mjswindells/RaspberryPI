import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

def on_message(client, userdata, message):
    temp = str(message.payload.decode("utf-8"))
    if temp == "1":
        GPIO.output(17,True)
    elif temp == "0":
        GPIO.output(17,False)
    else :
        print("message : " + temp)


client = mqtt.Client()
client.on_message = on_message

client.connect("broker.emqx.io", 1883)
client.subscribe("topic")

client.loop_forever()
