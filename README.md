# MQTT5 Shared Subscriptions demo

**Note** : Using AWS IoT Device SDK v2 for Python

Reference : https://github.com/aws/aws-iot-device-sdk-python-v2

<img src="images/mqttv5_sharedtopic.png"  width="70%" height="40%">

**Note** : Tested on awscrt-0.16.17 and awsiotsdk-1.14.1

# Testing status

| Publisher | Subscriber | Status | Files |
| --- | --- | --- | --- |
| MQTTV5 | MQTTV5 | [![Generic badge](https://img.shields.io/badge/TESTING-PASS-GREEN.svg)]() | **Publisher** : pub_mqtt5.py **Subscribers** : sub1_mqtt5.py and sub2_mqtt5.py |
| MQTTV3 | MQTTV3 | [![Generic badge](https://img.shields.io/badge/TESTING-PENDING-yellow.svg)]() |  |
| MQTTV5 | MQTTV3 | [![Generic badge](https://img.shields.io/badge/TESTING-PASS-GREEN.svg)]() | **Publisher** : pub_mqtt5.py **Subscribers** : sub1_mqtt3.py |
