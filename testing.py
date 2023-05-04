from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))


mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint="a4mkavb6ap6cy-ats.iot.us-west-2.amazonaws.com",
        port=8883,
        cert_filepath="./certs/subs/sub1/sub1-certificate.pem.crt",
        pri_key_filepath="./certs/subs/sub1/sub1-private.pem.key",
        ca_filepath="./certs/subs/sub1/AmazonRootCA1.pem",
        client_id="testingclient",
        clean_session=False,
        keep_alive_secs=30)

connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
connect_future.result()
print("Connected!")

message_topic = "$share/group1/topic1"

# Subscribe
print("Subscribing to topic '{}'...".format(message_topic))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=message_topic,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received)

subscribe_result = subscribe_future.result()
print("Subscribed with {}".format(str(subscribe_result['qos'])))

while True:
    time.sleep(0.0025)

# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")