import time
import board
import busio
import adafruit_adxl34x
import adafruit_bmp280
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import requests
import json

# GPIO and sensor setup
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)

# Sensors
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
accel = adafruit_adxl34x.ADXL345(i2c)
accel.enable_freefall_detection(threshold=10, time=25)
accel.enable_motion_detection(threshold=18)
accel.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
bmp280.sea_level_pressure = 1013.25

# Ultrasonic sensor
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# ADS1115 sensor
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)

# MQTT configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPICS = ["sensors/accelerometer", "sensors/bmp280", "sensors/ultrasonic", "sensors/ads1115"]

def on_publish(client, userdata, mid):
    print(f"Message published: {mid}")

mqttc = mqtt.Client()
mqttc.on_publish = on_publish

try:
    mqttc.connect(MQTT_BROKER, MQTT_PORT)
    mqttc.loop_start()
except Exception as e:
    print(f"Error connecting to MQTT: {e}")
    exit(1)

SERVER_URL = "http://192.168.1.204:8000" #Change to local IPV4

# Function to send data to FastAPI
def send_data_to_api(endpoint, data):
    url = f"{SERVER_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
        response.raise_for_status()
        print(f"Data sent to {endpoint}: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to {endpoint}: {e}")

# Function to measure distance with the ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    pulse_start, pulse_end = None, None
    timeout = time.time() + 1  # 1-second timeout to avoid infinite loops
    
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()
    
    if pulse_start is None or pulse_end is None:
        print("Error measuring distance")
        return -1  # Indicates an error

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Data publishing to MQTT and FastAPI
def publish_data():
    try:
        # Accelerometer
        x, y, z = accel.acceleration
        freefall_event = str(accel.events['freefall'])
        motion_event = str(accel.events['motion'])

        mqttc.publish(MQTT_TOPICS[0], f"Accelerometer reading: {x:.2f}, {y:.2f}, {z:.2f}")
        mqttc.publish(MQTT_TOPICS[0], f"Freefall event: {freefall_event}")
        mqttc.publish(MQTT_TOPICS[0], f"Motion detected: {motion_event}")

        accelerometer_data = {
            "x": x,
            "y": y,
            "z": z,
            "freefall_event": freefall_event,
            "motion_event": motion_event
        }
        send_data_to_api("accelerometer", accelerometer_data)

        # BMP280
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        altitude = bmp280.altitude
        
        mqttc.publish(MQTT_TOPICS[1], f"Temperature: {temperature:.1f} C")
        mqttc.publish(MQTT_TOPICS[1], f"Pressure: {pressure:.1f} hPa")
        mqttc.publish(MQTT_TOPICS[1], f"Altitude: {altitude:.2f} m")

        bmp280_data = {
            "temperature": temperature,
            "pressure": pressure,
            "altitude": altitude
        }
        send_data_to_api("bmp280", bmp280_data)

        # Ultrasonic sensor
        distance = measure_distance()
        if distance != -1:
            mqttc.publish(MQTT_TOPICS[2], f"Distance: {distance} cm")
            ultrasonic_data = {"distance_cm": distance}
            send_data_to_api("ultrasonic", ultrasonic_data)

        # ADS1115
        analog_value = channel.value
        voltage = channel.voltage
        mqttc.publish(MQTT_TOPICS[3], f"Analog value: {analog_value}, Voltage: {voltage:.2f} V")

        ads1115_data = {
            "analog_value": analog_value,
            "voltage": voltage
        }
        send_data_to_api("ads1115", ads1115_data)

    except Exception as e:
        print(f"Error publishing data: {e}")
        
# Main loop
try:
    while True:
        publish_data()
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    mqttc.disconnect()
    mqttc.loop_stop()
    print("Program terminated")
