#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import WLAN
from mqtt import MQTTClient
import machine
import time
import ubinascii
import configMQTT

def settimeout(duration): 
    pass

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)

# classical mac writing convention
print ("mac address = "+ ubinascii.hexlify(wlan.mac().sta_mac,':').decode())
strID = ubinascii.hexlify(wlan.mac().sta_mac,'').decode()
# hostname from the 4 last characters
hostNameID = ("N"+strID[-5:]).upper()
print("hostname = " + hostNameID)

wlan.connect(configMQTT.WIFI_SSID, auth=(WLAN.WPA, configMQTT.WIFI_PASS), timeout=5000)

while not wlan.isconnected(): 
     machine.idle()

print("Connected to Wifi\n")
client = MQTTClient("demo", "192.168.2.112", port=1883)
client.set_callback(sub_cb)
#client.settimeout = settimeout
client.connect()


# client = MQTTClient("device_id", "io.adafruit.com",user="your_username", password="your_api_key", port=1883)

# client.set_callback(sub_cb)
# client.connect()

#topics="/"+hostNameID+"/lights"
topics="LAICHE/lights"
print("publish to "+topics)

while True:
     print("Sending ON")
     client.publish(topic = topics, msg = "ON")
     time.sleep(2)
     print("Sending OFF")
     client.publish( topic = topics, msg = "OFF")
     time.sleep(2)
