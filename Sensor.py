# sensor.py
import random
import time

def generate_voltage():

    return round(random.uniform(0.0, 5.0), 3)

def run_sensor():
    print("Sensor started. Producing continuous voltage readings...")
    while True:
        voltage = generate_voltage()
        print(f"Voltage: {voltage} V")
        time.sleep(1)

if __name__ == "__main__":
    run_sensor()
