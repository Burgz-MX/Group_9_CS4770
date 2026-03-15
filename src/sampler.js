class Sampler {

  constructor(options = {}) {
    // Sampling interval for energy efficiency
    this.sampleIntervalMs = options.sampleIntervalMs || 5000;

    // Timeout for availability detection
    this.timeoutMs = options.timeoutMs || 10000;

    this.lastSampleTime = 0;
    this.lastReceivedTime = 0;
    this.degradedMode = false;
  }

  // Validate incoming sensor reading
  validateReading(reading) {
    if (!reading || typeof reading !== "object") {
      return { valid: false, error: "Reading must be an object" };
    }

    const { sensorId, voltage, timestamp } = reading;

    if (!sensorId || typeof sensorId !== "string") {
      return { valid: false, error: "sensorId must be a string" };
    }

    if (typeof voltage !== "number" || Number.isNaN(voltage)) {
      return { valid: false, error: "voltage must be a number" };
    }

    if (!timestamp || Number.isNaN(Date.parse(timestamp))) {
      return { valid: false, error: "timestamp must be a valid ISO string" };
    }

    return { valid: true };
  }

  // Determine if reading should be sampled
  shouldSample(currentTime) {
    return currentTime - this.lastSampleTime >= this.sampleIntervalMs;
  }

  // Main sampler logic
  processReading(reading) {

    const validation = this.validateReading(reading);
    if (!validation.valid) {
      return {
        status: "error",
        message: validation.error
      };
    }

    const now = Date.now();
    this.lastReceivedTime = now;

    // Energy efficiency: skip readings between intervals
    if (!this.shouldSample(now)) {
      return {
        status: "skipped",
        sensorId: reading.sensorId,
        message: "Reading skipped due to sampling interval"
      };
    }

    this.lastSampleTime = now;
    this.degradedMode = false;

    return {
      status: "accepted",
      sensorId: reading.sensorId,
      sampledVoltage: reading.voltage,
      timestamp: reading.timestamp
    };
  }

  // Availability monitoring (detect missing sensor data)
  checkAvailability() {

    const now = Date.now();

    if (this.lastReceivedTime !== 0 &&
        now - this.lastReceivedTime > this.timeoutMs) {

      this.degradedMode = true;

      return {
        degradedMode: true,
        message: "Sensor timeout detected"
      };
    }

    return {
      degradedMode: false,
      message: "System operating normally"
    };
  }

}

module.exports = Sampler;
