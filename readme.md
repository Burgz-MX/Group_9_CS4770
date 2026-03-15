# Sampler Component API

The Sampler receives raw voltage readings from the Sensor and processes them at controlled intervals before forwarding them to downstream components.

##Pipeline:

Sensor → Sampler → Transformer → REST API → Database

---

## Endpoint
POST /sample

---

## Input JSON Example

{
  "sensorId": "sensor-1",
  "voltage": 2.75,
  "timestamp": "2026-03-15T18:30:00Z"
}

---

## Output JSON Example

{
  "status": "accepted",
  "sensorId": "sensor-1",
  "sampledVoltage": 2.75,
  "timestamp": "2026-03-15T18:30:00Z"
}

---

## Design Explanation

The Sampler exposes a JSON-based HTTPS endpoint that receives voltage readings from sensors.  
It validates incoming data and processes readings only at fixed intervals to improve energy efficiency.  
Timeout detection is used to detect missing sensor readings and support system availability.
