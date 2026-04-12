# Sampler Component API

The Sampler receives raw voltage readings from the Sensor and processes them at controlled intervals before forwarding them to downstream components.

## Pipeline:

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




# Transformer Component – API Design

The Transformer component receives sampled voltage data from the Sampler and converts it into temperature values.  
The interface uses JSON over HTTPS so that it stays consistent with the Weather Station pipeline.

Pipeline:  
Sensor → Sampler → Transformer → REST API → Database

## Endpoint
POST /transform

## Input JSON Example

{
  "sensorId": "sensor-1",
  "sampledVoltage": 2.75,
  "timestamp": "2026-03-20T16:00:00Z"
}

## Output JSON Example

{
  "sensorId": "sensor-1",
  "temperature": 27.5,
  "unit": "C",
  "timestamp": "2026-03-20T16:00:00Z",
  "status": "success"
}

## Design Explanation

The Transformer exposes a simple JSON-based endpoint that accepts sampled voltage values and returns converted temperature values.
The design is kept consistent with the Sampler API so that integration in the pipeline remains straightforward.
A simple formula is used for conversion to prioritize correctness, readability, and easy testing.


# REST API – Temperature Storage Interface

The REST API receives temperature data from the Transformer, validates it, stores it in the database, and returns a confirmation response.  
The interface uses JSON over HTTPS and is designed to stay simple and consistent with the Weather Station pipeline.

Pipeline:  
Sensor → Sampler → Transformer → REST API → Database

## Endpoint
POST /temperature

## Input JSON Example
json
{
  "temperature": 24.5,
  "timestamp": "2026-03-10T14:20:00Z"
}
## Output JSON Example
{
  "status": "stored",
  "id": 104
}

## Design Explanation

The REST API accepts temperature data in JSON format so it can be easily called by the Transformer.
The service validates the input before storing it in the database to avoid bad records.
A short confirmation response is returned so the caller knows the data was stored successfully.
