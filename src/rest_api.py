from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "weatherdb")
DB_USER = os.getenv("DB_USER", "weatheruser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "weatherpass")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS temperature_readings (
            id SERIAL PRIMARY KEY,
            temperature FLOAT NOT NULL,
            timestamp VARCHAR(50) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/temperature", methods=["POST"])
def store_temperature():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON"
        }), 400

    temperature = data.get("temperature")
    timestamp = data.get("timestamp")

    if not isinstance(temperature, (int, float)):
        return jsonify({
            "status": "error",
            "message": "temperature must be a number"
        }), 400

    if not timestamp or not isinstance(timestamp, str):
        return jsonify({
            "status": "error",
            "message": "timestamp must be a string"
        }), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO temperature_readings (temperature, timestamp) VALUES (%s, %s) RETURNING id;",
        (temperature, timestamp)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "stored",
        "id": new_id
    }), 200


@app.route("/records", methods=["GET"])
def get_records():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, temperature, timestamp FROM temperature_readings ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "temperature": row[1],
            "timestamp": row[2]
        })

    return jsonify(results), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=6000, debug=True)
