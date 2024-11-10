# Proyecto_xrover
Proyecto final de Implementación de internet de las cosas - ITESM CCM

Instrucciones de instalación

Nota!
Antes de usar del Raspberry pi4 es importante ejecuar estas instrucciones:
  - sudo apt-get update
  - sudo apt-get upgrade
Y para comprobar que el Raspberry pi4 detecte los sensores ejecutar:
  - sudo i2cdetect -y 1

El circuito se arma como se encuentra en diagrama_xrover.png

1. Salir del entorno virtual del Raspberry pi4 con estas instrucciones:
     - ls /usr/bin/python* (observar la versión de python instalada, ej: python 3.11.2)
     - sudo rm /usr/lib/python3.xx/EXTERNALLY-MANAGED ( se intercambia por la versión instalada, ej: sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED)
3. En el Raspberry pi4 instalar:
     - sudo pip3 install adafruit-circuitpython-ads1x15
     - sudo pip3 install adafruit-circuitpython-bmp280
     - pip3 install paho-mqtt
     - sudo apt install mosquitto mosquitto-clients
     - sudo systemctl enable mosquitto.service
   Si Thonny no detecta las bibliotecas:
    - Tools
    - Manage Packages
    - En la ventana que se abre, buscar 'nombre_biblioteca' e instalar.
