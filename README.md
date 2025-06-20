# Real-Time Environment Monitoring System

An end-to-end **IoT and Data Visualization** project that simulates real-time environmental data (temperature, humidity) using virtual sensors, publishes it over MQTT, stores it in **InfluxDB**, and visualizes it using **Grafana** dashboards with real-time alerts.

---

## 🚀 Features

- Simulated IoT sensor data using Python
- MQTT protocol for real-time data transfer
- Node-RED flow for parsing, formatting, and routing data
- InfluxDB (Docker) for time-series data storage
- Grafana dashboards for real-time insights
- Threshold-based alerts using Grafana Alerting
- Flux queries for advanced analytics

---

## 🧱 Architecture Overview

```text
[ Python Sensor Simulator ]
          |
       MQTT Broker (Mosquitto)
          |
       Node-RED
        |- JSON Parsing
        |- Data Formatting (InfluxDB Line Protocol)
        |- Extract Fields
        |- Store in InfluxDB
        |- Debug + Charts
          |
       InfluxDB (Docker)
          |
       Grafana (Docker)
        |- Dashboards
        |- Alerts (Rain Prediction, Heatwave, Coldwave)
```

---

## 📦 Repository Structure

```text
real-time-environment-monitoring/
├── sensor_simulator.py       # Python script for simulating sensors
├── node_red_flow.json        # Exported Node-RED flow
├── influxdb-docker-compose.yml # Docker Compose for InfluxDB and Grafana
├── grafana_dashboard.json    # Grafana dashboard JSON
├── alerts_flux_queries.md    # Flux alert expressions
├── README.md                 # Project overview and setup guide
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/real-time-environment-monitoring.git
cd real-time-environment-monitoring
```

### 2. Start Docker Services

```bash
docker-compose -f influxdb-docker-compose.yml up -d
```

### 3. Import Node-RED Flow

- Launch Node-RED at `http://localhost:1880`
- Import `node_red_flow.json`
- Deploy the flow

### 4. Run the Sensor Simulator

```bash
python sensor_simulator.py
```

### 5. Set Up Grafana

- Access Grafana at `http://localhost:3000`
- Login (default: admin/admin)
- Add InfluxDB as a data source
- Import `grafana_dashboard.json` for visualizations

### 6. Alerts & Analytics

- Navigate to Alerting → Manage
- Use Flux queries from `alerts_flux_queries.md` to set up:
  - 🌧 Rain prediction (based on humidity)
  - 🔥 Heatwave (high temperature)
  - ❄️ Coldwave (low temperature)

---

## 📊 Metrics Visualized

- Live Temperature Trends (line chart)
- Humidity Levels Over Time
- Last Recorded Sensor Data (single stat)
- Dynamic Sensor ID Switching (based on topic)
- Alert thresholds with visual markers

---

## 🛠 Technologies Used

- **Python** — Sensor simulation
- **Node-RED** — Workflow automation & parsing
- **MQTT (Mosquitto)** — Messaging protocol
- **InfluxDB** — Time-series database
- **Grafana** — Dashboards and alerts
- **Docker** — Environment setup and orchestration

---

## 📌 Notes

- Each simulated sensor has a dynamic ID (`kiit_<random>`), which is handled in Node-RED and InfluxDB tagging automatically.
- Timestamp conversion is handled using `timestamp * 1000` for Influx compatibility.
- Alerts use Grafana-managed rules based on Flux expressions.

---

## 🧪 Future Improvements

- Add air quality and pressure sensors
- Enable long-term trend analysis
- Integrate ML model for weather classification
- Mobile-friendly Grafana dashboards

---

## 📝 License

This project is licensed under the MIT License. See `LICENSE` for more details.
