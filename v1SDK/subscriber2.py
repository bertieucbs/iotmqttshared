# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import os
import sys
import uuid
import json
import logging
from random import seed
from random import randint

# Configure logging

logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print(client)
    print(userdata)
    print("Subscriber 2 : Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def mySubackCallback(mid, data):
    print("mid")
    print(mid)
    print("data")
    print(data)

def myPubackCallback(mid):
    print("mid")
    print(mid)
    

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("subscriber2")

myMQTTClient.configureEndpoint("a4mkavb6ap6cy-ats.iot.us-west-2.amazonaws.com", 8883)

myMQTTClient.configureCredentials("./certs/subs/sub2/AmazonRootCA1.pem", "./certs/subs/sub2/sub2-private.pem.key", "./certs/subs/sub2/sub2-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.subscribe("$share/group1/topic1", 1, customCallback)

while True:
    time.sleep(0.0025)

print("Disconnecting...")
  

myMQTTClient.disconnect()