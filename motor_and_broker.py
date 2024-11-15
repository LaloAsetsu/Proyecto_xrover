import time
import board
import busio
import adafruit_adxl34x
import adafruit_bmp280
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO and sensor setup
GPIO.setmode(GPIO.BCM)
i2c = busio.I2C(board.SCL, board.SDA)

# Sensors setup
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
accel = adafruit_adxl34x.ADXL345(i2c)
accel.enable_freefall_detection(threshold=10, time=25)
accel.enable_motion_detection(threshold=18)
accel.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
bmp280.sea_level_pressure = 1013.25

# Ultrasonic sensor setup
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# ADS1115 sensor setup
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)

# Motor pins (using GPIO.BCM)
MotorA1 = 22  # Entrada
MotorA2 = 27  # Entrada
MotorA3 = 17  # Habilitar

MotorB1 = 21   # Entrada
MotorB2 = 20   # Entrada
MotorB3 = 16  # Habilitar

# Motor setup
GPIO.setup(MotorA1, GPIO.OUT)
GPIO.setup(MotorA2, GPIO.OUT)
GPIO.setup(MotorA3, GPIO.OUT)
GPIO.setup(MotorB1, GPIO.OUT)
GPIO.setup(MotorB2, GPIO.OUT)
GPIO.setup(MotorB3, GPIO.OUT)

# MQTT configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPICS = ["sensors/accelerometer", "sensors/ads1115", "sensors/bmp280", "sensors/ultrasonic", "sensors/direction"]

def stop():
    """Stop both motors."""
    print("stop")
    GPIO.output(MotorA1, GPIO.LOW)
    GPIO.output(MotorA2, GPIO.LOW)
    GPIO.output(MotorB1, GPIO.LOW)
    GPIO.output(MotorB2, GPIO.LOW)
    GPIO.output(MotorA3, GPIO.LOW)
    GPIO.output(MotorB3, GPIO.LOW)

def on_message(client, userdata, msg):
    """Car control based on MQTT message."""
    try:
        direction = msg.payload.decode()
    except UnicodeDecodeError:
        print("Error decoding message")
        return

    if direction == "w":
        print("forward")
        GPIO.output(MotorA1, GPIO.LOW)
        GPIO.output(MotorA2, GPIO.HIGH)
        GPIO.output(MotorA3, GPIO.HIGH)
        GPIO.output(MotorB1, GPIO.LOW)
        GPIO.output(MotorB2, GPIO.HIGH)
        GPIO.output(MotorB3, GPIO.HIGH)
    elif direction == "s":
        print("backward")
        GPIO.output(MotorA1, GPIO.HIGH)
        GPIO.output(MotorA2, GPIO.LOW)
        GPIO.output(MotorA3, GPIO.HIGH)
        GPIO.output(MotorB1, GPIO.HIGH)
        GPIO.output(MotorB2, GPIO.LOW)
        GPIO.output(MotorB3, GPIO.HIGH)

    elif direction == "d":
        print("right")
        GPIO.output(MotorA1, GPIO.LOW)
        GPIO.output(MotorA2, GPIO.HIGH)
        GPIO.output(MotorA3, GPIO.HIGH)
        GPIO.output(MotorB3, GPIO.LOW)

    elif direction == "a":
        print("left")
        GPIO.output(MotorB1, GPIO.LOW)
        GPIO.output(MotorB2, GPIO.HIGH)
        GPIO.output(MotorB3, GPIO.HIGH)
        GPIO.output(MotorA3, GPIO.LOW)

    else:
        print("Invalid command")
    
    time.sleep(2)
    stop()

# Function to measure distance with the ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    pulse_start, pulse_end = None, None
    timeout = time.time() + 1

    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    if pulse_start is None or pulse_end is None:
        logging.error("Error measuring distance")
        return -1 

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# Data publishing to MQTT
def publish_data():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # Accelerometer
        x, y, z = accel.acceleration
        freefall_event = str(accel.events['freefall'])
        motion_event = str(accel.events['motion'])
        mqttc.publish(MQTT_TOPICS[0], f"accelerometer_{x:.2f}_{y:.2f}_{z:.2f}_{freefall_event}_{motion_event}_{current_time}")

        # BMP280
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        altitude = bmp280.altitude
        mqttc.publish(MQTT_TOPICS[2], f"bmp280_{temperature:.1f}_{pressure:.1f}_{altitude:.2f}_{current_time}")

        # Ultrasonic
        distance = measure_distance()
        if distance != -1:
            mqttc.publish(MQTT_TOPICS[3], f"ultrasonic_{distance}_{current_time}")

        # ADS1115
        analog_value = channel.value
        voltage = channel.voltage
        mqttc.publish(MQTT_TOPICS[1], f"ads1115_{analog_value}_{voltage:.2f}_{current_time}")

    except Exception as e:
        logging.error(f"Error publishing data: {e}")

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect(MQTT_BROKER, MQTT_PORT)
mqttc.loop_start()
mqttc.subscribe(MQTT_TOPICS[4])

try:
    while True:
        publish_data()
        time.sleep(5)
except KeyboardInterrupt:
    pass
except Exception as e:
    logging.error(f"unexpected error: {e}")
finally:
    mqttc.loop_stop()
    mqttc.disconnect()
    GPIO.cleanup()
    logging.info("Program terminated")

