import paho.mqtt.publish as publish
import json
import time
import random
import uuid
import requests
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# ------------------ STEP 1: Setup device ID ------------------
try:
    with open("device_id.txt", "r") as f:
        UNIQUE_ID = f.read().strip()
except FileNotFoundError:
    UNIQUE_ID = f"kiit_{uuid.uuid4().hex[:6]}"
    with open("device_id.txt", "w") as f:
        f.write(UNIQUE_ID)

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = f"iot_project/sensors/{UNIQUE_ID}/data"

print(f"Your device ID: {UNIQUE_ID}")
print(f"Using topic: {TOPIC}")

# ------------------ STEP 2: Train ML model for rain prediction ------------------
def train_dummy_model():
    data = pd.DataFrame({
        "temperature": np.random.uniform(10, 40, 1000),
        "humidity": np.random.uniform(30, 100, 1000)
    })
    data["rain"] = ((data["humidity"] > 80) & (data["temperature"] < 30)).astype(int)
    X = data[["temperature", "humidity"]]
    y = data["rain"]
    model = LogisticRegression()
    model.fit(X, y)
    return model

model = train_dummy_model()

# ------------------ STEP 3: Classify alerts ------------------
def classify_conditions(temp, humidity, rain_pred):
    alerts = []
    if temp < 15:
        alerts.append("🥶 Cold Wave")
    if temp > 38:
        alerts.append("🔥 Heat Wave")
    if rain_pred:
        alerts.append("🌧 Rain Likely")
    return alerts if alerts else ["✅ Normal"]

# ------------------ STEP 4: Send alerts to InfluxDB ------------------
def send_alert_to_influx(alert_text, sensor_id, timestamp):
    line = f'weather_alert,sensor_id={sensor_id} status="{alert_text}" {timestamp}000000000'
    try:
        response = requests.post(
            url="http://localhost:8086/write?db=iot_data",
            data=line,
            headers={"Content-Type": "text/plain"}
        )
        if response.status_code != 204:
            print(f"❌ InfluxDB error: {response.text}")
        else:
            print(f"✅ Alert sent to InfluxDB: {alert_text}")
    except Exception as e:
        print(f"❌ Error connecting to InfluxDB: {e}")

# ------------------ STEP 5: Main loop ------------------
while True:
    # Simulate sensor values
    payload = {
        "sensor_id": UNIQUE_ID,
        "temperature": round(random.uniform(10, 42), 2),
        "humidity": round(random.uniform(30, 95), 2),
        "timestamp": int(time.time())
    }

    # Publish via MQTT
    try:
        publish.single(
            TOPIC,
            payload=json.dumps(payload),
            hostname=BROKER,
            port=PORT,
            client_id=f"pub_{UNIQUE_ID}",
            retain=False
        )
        print(f"📡 Published MQTT: {payload}")
    except Exception as e:
        print(f"❌ MQTT error: {str(e)}")

    # Predict rain
    X_test = [[payload["temperature"], payload["humidity"]]]
    rain_prediction = bool(model.predict(X_test)[0])

    # Classify & send alert
    alerts = classify_conditions(payload["temperature"], payload["humidity"], rain_prediction)
    alert_text = " | ".join(alerts)
    send_alert_to_influx(alert_text, payload["sensor_id"], payload["timestamp"])

    time.sleep(10)

