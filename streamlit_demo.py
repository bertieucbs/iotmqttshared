# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awsiot import mqtt5_client_builder
from awscrt import mqtt5, http
import threading
from concurrent.futures import Future
import time
import json

import streamlit as st
st.title('Uber pickups in NYC')


TIMEOUT = 100
message_topic = "$share/group1/topic1"
future_connection_success = Future()
received_count = 0

# Callback when any publish is received
def on_publish_received(publish_packet_data):
    publish_packet = publish_packet_data.publish_packet
    assert isinstance(publish_packet, mqtt5.PublishPacket)
    print("Received message from topic'{}':{}".format(publish_packet.topic, publish_packet.payload))
    st.write(publish_packet.payload)
    global received_count
    received_count += 1
    print("{}{}".format("received_count sub1--", received_count))


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
        cert_filepath="./certs/subs/sub1/sub1-certificate.pem.crt",
        pri_key_filepath="./certs/subs/sub1/sub1-private.pem.key",
        ca_filepath="./certs/pubs/AmazonRootCA1.pem",
        on_publish_received=on_publish_received,
        on_lifecycle_stopped=on_lifecycle_stopped,
        on_lifecycle_connection_success=on_lifecycle_connection_success,
        on_lifecycle_connection_failure=on_lifecycle_connection_failure,
        client_id="sub1")

print("MQTT5 Client Created")

client.start()

    # Subscribe

print("Subscribing to topic '{}'...".format(message_topic))
subscribe_future = client.subscribe(subscribe_packet=mqtt5.SubscribePacket(
        subscriptions=[mqtt5.Subscription(
            topic_filter=message_topic,
            qos=mqtt5.QoS.AT_LEAST_ONCE)]
    ))
suback = subscribe_future.result(TIMEOUT)
print("Subscribed with {}".format(suback.reason_codes))





while True:
    time.sleep(0.0025)

# Unsubscribe

print("Unsubscribing from topic '{}'".format(message_topic))
unsubscribe_future = client.unsubscribe(unsubscribe_packet=mqtt5.UnsubscribePacket(
topic_filters=[message_topic]))
unsuback = unsubscribe_future.result(TIMEOUT)
print("Unsubscribed with {}".format(unsuback.reason_codes))

print("Stopping Client")

client.stop()

print("Client Stopped!")