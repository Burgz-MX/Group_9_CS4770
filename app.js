const express = require("express")
const Sampler = require("./sampler")

const app = express()
const port = 3000

const sampler = new Sampler()

app.use(express.json())

app.post("/sample", (req, res) => {

    const result = sampler.processReading(req.body)

    if (result.status === "error") {
        return res.status(400).json(result)
    }

    res.json(result)
})

app.get("/health", (req, res) => {
    res.json(sampler.checkAvailability())
})

app.listen(port, () => {
    console.log("Sampler running on port", port)
})
