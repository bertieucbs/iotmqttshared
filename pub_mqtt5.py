# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, http
import threading
from concurrent.futures import Future
import time
import json
from random import seed
from random import randint
import logging
from awscrt import io

#io.init_logging(io.LogLevel.Trace, 'stdout')



TIMEOUT = 100
future_connection_success = Future()

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))
    global received_count
    received_count += 1


# Callback for the lifecycle event Stopped
def on_lifecycle_stopped(lifecycle_stopped_data: mqtt5.LifecycleStoppedData):
    print("Lifecycle Stopped")
    global future_stopped
    future_stopped.set_result(lifecycle_stopped_data)


# Callback for the lifecycle event Connection Success
def on_lifecycle_connection_success(lifecycle_connect_success_data: mqtt5.LifecycleConnectSuccessData):
    print("Lifecycle Connection Success")
    global future_connection_success
    future_connection_success.set_result(lifecycle_connect_success_data)


# Callback for the lifecycle event Connection Failure
def on_lifecycle_connection_failure(lifecycle_connection_failure: mqtt5.LifecycleConnectFailureData):
    print("Lifecycle Connection Failure")
    print("Connection failed with exception:{}".format(lifecycle_connection_failure.exception))


    # Create MQTT5 client
client = mqtt5_client_builder.mtls_from_path(
        endpoint="a4mkavb6ap6cy-ats.iot.us-west-2.amazonaws.com",
        port=8883,
        cert_filepath="./certs/pubs/publisher_mqtt_shared-certificate.pem.crt",
        pri_key_filepath="./certs/pubs/publisher_mqtt_shared-private.pem.key",
        ca_filepath="./certs/pubs/AmazonRootCA1.pem",
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        client_id="mqtt5_publisherclient")
print("MQTT5 Client Created")

client.start()

message_string = "this is a test"
message_topic = "topic1"

for x in range(1000):

    #payLoad = '{ "name":"John", "age":30, "city":"New York"}'
    payLoad = {}
    temp = randint(20, 40)
    vib = randint(100, 400)
    payLoad['sample_temperature'] = temp
    payLoad['sample_vibration'] = vib
    messageJson = json.dumps(payLoad)
    finalPayload = json.dumps(payLoad)
    print(messageJson)
    publish_future = client.publish(mqtt5.PublishPacket(
                topic=message_topic,
                payload=finalPayload,
                qos=mqtt5.QoS.AT_LEAST_ONCE
            ))
    time.sleep(2)

publish_completion_data = publish_future.result(TIMEOUT)
print("PubAck received with {}".format(repr(publish_completion_data.puback.reason_code)))

print("Stopping Client")
client.stop()