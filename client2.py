#!/usr/bin/env python3
import socket 
from time import sleep

from ev3dev2.motor import LargeMotor 
from ev3dev2.motor import OUTPUT_A
from ev3dev2.sound import Sound
sound = Sound()

base_motor = LargeMotor(OUTPUT_A)

HOST = 'C0:3C:59:D8:CE:8E'
PORT = 5

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server_address = (HOST, PORT)  # Replace with your server's IP and port
client.connect(server_address)

client.send("Hello from client!".encode("utf-8"))

while True:
    message = client.recv(1024).decode("utf-8")
    if message == "Run":
        base_motor.on(speed=30)
        sleep(0.1)
        base_motor.on(speed=-30)
        sleep(0.1)
        base_motor.stop()

    if message == "Beep":
        sound.beep()

    if message == "Exit":
        break
client.close()
    