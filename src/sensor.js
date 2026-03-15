const axios = require("axios")

function generateReading() {

    return {
        sensorId: "sensor-1",
        voltage: Math.random() * 5,
        timestamp: new Date().toISOString()
    }
}

async function sendReading() {

    const reading = generateReading()

    try {

        const response = await axios.post(
            "http://localhost:3000/sample",
            reading
        )

        console.log("Sensor Sent:", reading)
        console.log("Sampler Response:", response.data)

    } catch (error) {

        console.log("Error sending reading")
    }
}

setInterval(sendReading, 2000)
