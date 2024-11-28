import time
from DatabaseManager import DatabaseManager
import paho.mqtt.client as mqtt

# Inicializar conexión a la base de datos
db_manager = DatabaseManager('localhost', 'proyecto_xrover', 'root', 'Lalito24571$')

# Función cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al broker")
        # Suscribirse a los tópicos una vez conectado
        client.subscribe("sensors/ads1115")
        client.subscribe("sensors/accelerometer")
        client.subscribe("sensors/ultrasonic")
        client.subscribe("sensors/bmp280")
    else:
        print(f"Error al conectarse al broker. Código de error: {rc}")

# Función para manejar mensajes entrantes
def on_message(client, userdata, msg):
    try:
        msg_decoded = msg.payload.decode()
        print(f"Mensaje recibido en {msg.topic}: {msg_decoded}")
        msg_split = msg_decoded.split("_")
        sensor = msg_split[0]

        if sensor == "ads1115" and len(msg_split) >= 4:
            valor1, valor2, valor3 = msg_split[1:4]
            db_manager.insert_ads1115(valor1, valor2, valor3)
            print(f"ADS1115 - Valor1: {valor1}, Valor2: {valor2}, Valor3: {valor3}")

        elif sensor == "accelerometer" and len(msg_split) >= 7:
            valor1, valor2, valor3, valor4, valor5, valor6 = msg_split[1:7]
            db_manager.insert_accelerometer(valor1, valor2, valor3, valor4, valor5, valor6)
            print(f"Accelerometer - Valores: {valor1}, {valor2}, {valor3}, {valor4}, {valor5}, {valor6}")

        elif sensor == "bmp280" and len(msg_split) >= 5:
            valor1, valor2, valor3, valor4 = msg_split[1:5]
            db_manager.insert_bmp280(valor1, valor2, valor3, valor4)
            print(f"BMP280 - Temperatura: {valor1}, Presión: {valor2}, Altitud: {valor3}")

        elif sensor == "ultrasonic" and len(msg_split) >= 3:
            valor1, valor2 = msg_split[1:3]
            db_manager.insert_ultrasonic(valor1, valor2)
            print(f"Ultrasonic - Distancia: {valor1}, Tiempo: {valor2}")

        else:
            print("Mensaje no reconocido o incompleto")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Configuración del cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    # Conectar al broker
    mqtt_client.connect("broker.hivemq.com", 1883)
    mqtt_client.loop_start()

    print("Esperando mensajes...")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupción por teclado. Saliendo...")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Cliente desconectado")
