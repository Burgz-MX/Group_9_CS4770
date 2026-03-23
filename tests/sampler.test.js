const Sampler = require("../src/sampler")

test("accepts valid reading", () => {

    const sampler = new Sampler(0)

    const result = sampler.processReading({
        sensorId: "sensor-1",
        voltage: 3.2,
        timestamp: new Date().toISOString()
    })

    expect(result.status).toBe("accepted")
})

test("rejects invalid data", () => {

    const sampler = new Sampler()

    const result = sampler.processReading({
        sensorId: "sensor-1",
        voltage: "bad"
    })

    expect(result.status).toBe("error")
})
