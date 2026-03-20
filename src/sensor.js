const axios = require("axios");

function generateReading() {
  return {
    sensorId: "sensor-1",
    voltage: Number((Math.random() * 5).toFixed(2)),
    timestamp: new Date().toISOString()
  };
}

async function sendReading() {
  const reading = generateReading();

  try {
    const response = await axios.post("http://localhost:3000/sample", reading, {
      headers: { "Content-Type": "application/json" }
    });

    console.log("Sensor sent:", reading);
    console.log("Pipeline response:", JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error("Failed to send reading:", error.response?.data || error.message);
  }
}

setInterval(sendReading, 2000);
