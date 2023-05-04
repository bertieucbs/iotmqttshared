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
'''
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
'''

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print(client)
    print(userdata)
    print("Received a new message: ")
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
myMQTTClient = AWSIoTMQTTClient("myClientID")

myMQTTClient.configureEndpoint("a4mkavb6ap6cy-ats.iot.us-west-2.amazonaws.com", 8883)

myMQTTClient.configureCredentials("./certs/pubs/AmazonRootCA1.pem", "./certs/pubs/publisher_mqtt_shared-private.pem.key", "./certs/pubs/publisher_mqtt_shared-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()

#myMQTTClient.subscribe('/aws/test/topic', 1, customCallback)

for x in range(100):

    #payLoad = '{ "name":"John", "age":30, "city":"New York"}'
    payLoad = {}
    temp = randint(20, 40)
    vib = randint(100, 400)
    payLoad['sample_temperatusre'] = temp
    payLoad['sample_vibration'] = vib
    messageJson = json.dumps(payLoad)
    finalPayload = json.dumps(payLoad)
    print(messageJson)
    myMQTTClient.publish("topic1", finalPayload,1)
    time.sleep(2)



print("Disconnecting...")
  

myMQTTClient.disconnect()