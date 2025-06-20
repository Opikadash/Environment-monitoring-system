import paho.mqtt.client as mqtt

TOPIC = "iot_project/sensors/+/data"
BROKER = "test.mosquitto.org"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}:")
    print(msg.payload.decode())

client = mqtt.Client(protocol=mqtt.MQTTv311)
# and prints the received messages to the console.
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
# This code is a simple MQTT client that subscribes to a specific topic
import csv
import os
import json
from datetime import datetime

# Create CSV file with headers if it doesn't exist
csv_file = "sensor_data.csv"
if not os.path.isfile(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "sensor_id", "temperature", "humidity"])

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}:")
    data = json.loads(msg.payload.decode())

    # Convert UNIX timestamp to human-readable format
    human_time = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

    # Append to CSV
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([human_time, data["sensor_id"], data["temperature"], data["humidity"]])
    
    print(f"Saved to CSV: {data}")
# Initialize MQTT client
