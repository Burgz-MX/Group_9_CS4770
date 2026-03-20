const express = require("express");
const axios = require("axios");
const Sampler = require("./sampler");

const app = express();
const port = 3000;

const sampler = new Sampler({
  sampleIntervalMs: 5000,
  timeoutMs: 10000
});

app.use(express.json());

app.post("/sample", async (req, res) => {
  const result = sampler.processReading(req.body);

  if (result.status === "error") {
    return res.status(400).json(result);
  }

  if (result.status === "skipped") {
    return res.status(200).json(result);
  }

  try {
    const transformerResponse = await axios.post("http://localhost:5000/transform", {
      sensorId: result.sensorId,
      sampledVoltage: result.sampledVoltage,
      timestamp: result.timestamp
    });

    return res.status(200).json({
      sampler: result,
      transformer: transformerResponse.data
    });
  } catch (error) {
    return res.status(500).json({
      status: "error",
      message: "Transformer service unavailable",
      details: error.message
    });
  }
});

app.get("/health", (req, res) => {
  const health = sampler.checkAvailability();
  res.status(200).json(health);
});

app.listen(port, () => {
  console.log(`Sampler API running on port ${port}`);
});
