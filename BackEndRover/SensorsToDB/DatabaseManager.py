import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, database, user, password):
        # Inicializa los parámetros de conexión
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            # Intenta conectar a la base de datos
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to the database")
        except Error as e:
            # Maneja errores de conexión
            print(f"Error connecting to database: {e}")
            self.connection = None

    def disconnect(self):
        # Desconecta de la base de datos si está conectado
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from the database")

    def insert_ads1115(self, value1, value2, value3):
        # Inserta datos en la tabla ads1115
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            query = """INSERT INTO ads1115 (analog_value, voltage, fecha) VALUES (%s, %s, %s)"""
            values = (value1, value2, value3)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Inserted ADS1115 data")
        except Error as e:
            # Maneja errores de inserción
            print(f"Error inserting ADS1115 data: {e}")

    def insert_accelerometer(self, value1, value2, value3, value4, value5, value6):
        # Inserta datos en la tabla accelerometer
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            query = """INSERT INTO accelerometer (x, y, z, freefall_event, motion_event, fecha) VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (value1, value2, value3, value4, value5, value6)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Inserted accelerometer data")
        except Error as e:
            # Maneja errores de inserción
            print(f"Error inserting accelerometer data: {e}")

    def insert_bmp280(self, value1, value2, value3, value4):
        # Inserta datos en la tabla bmp280
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            query = """INSERT INTO bmp280 (temperature, pressure, altitude, fecha) VALUES (%s, %s, %s, %s)"""
            values = (value1, value2, value3, value4)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Inserted BMP280 data")
        except Error as e:
            # Maneja errores de inserción
            print(f"Error inserting BMP280 data: {e}")

    def insert_ultrasonic(self, value1, value2):
        # Inserta datos en la tabla ultrasonic
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            query = """INSERT INTO ultrasonic (distance_cm, fecha) VALUES (%s, %s)"""
            values = (value1, value2)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Inserted ultrasonic data")
        except Error as e:
            # Maneja errores de inserción
            print(f"Error inserting ultrasonic data: {e}")
