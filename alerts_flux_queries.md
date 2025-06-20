### 🌧 Rain Prediction Alert (Humidity > 85%)
```flux
from(bucket: "iot_data")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "humidity")
  |> mean()

### Heat wave (Temperature>35)
```flux
from(bucket: "iot_data")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> mean()

### Cold Wave (Temperature<-12)
```flux
from(bucket: "iot_data")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> mean()
