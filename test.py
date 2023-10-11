#!/usr/bin/env python3

import socket
from time import sleep
import threading

from ev3dev2.motor import (MediumMotor, LargeMotor,
                            OUTPUT_A, OUTPUT_B, OUTPUT_C)

# The MAC address of a Bluetooth adapter on the server
HOST = 'C0:3C:59:D8:CE:8E'
# The port used by the server
PORT = 6
# The size of the header
HEADER_SIZE = 64
# The format of the message
FORMAT = "ASCII"

base_pos = 0
elbow_pos = 0
gripper_pos = ''
running = True
motor_speed = 10

# Create the client socket and connect to the server
client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect((HOST, PORT))
# Send message to the server
client.send("Arm ready!".encode("ASCII"))

class MotorThread(threading.Thread):
    def __init__(self):
        self.base_motor = LargeMotor(OUTPUT_A)
        self.elbow_motor = LargeMotor(OUTPUT_B)
        self.gripper_motor = MediumMotor(OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.base_motor.reset()
            self.elbow_motor.reset()
            self.gripper_motor.reset()
            
            while running:

                bp = self.base_motor.position
                ep = self.elbow_motor.position

                if abs(bp - base_pos) > 10:
                    if bp < base_pos:
                        self.base_motor.on(speed=motor_speed)
                    if bp > base_pos:
                        self.base_motor.on(speed=-motor_speed)
                else:
                    self.base_motor.stop()

                if abs(ep - elbow_pos) > 10:
                    if ep > elbow_pos:
                        self.elbow_motor.on(speed=-motor_speed)
                    if ep < elbow_pos:
                        self.elbow_motor.on(speed=motor_speed)
                else:
                    self.elbow_motor.stop()

                gp = self.gripper_motor.position

                if gripper_pos == '00000':
                    self.gripper_motor.on(speed=10)
                    if gp > 25:
                        self.gripper_motor.stop()

                if gripper_pos == '11111':
                    self.gripper_motor.on(speed=-10)
                    if gp < -25:
                        self.gripper_motor.stop()
                

            self.elbow_motor.stop()
            self.base_motor.stop()
            self.gripper_motor.stop()
            
        except Exception as e:
            self.elbow_motor.stop()
            self.base_motor.stop()
            self.gripper_motor.stop()
            print("Motors stopped.")
            print("An error occurred:", str(e))

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

while True:
    
    try:
        msg_length = client.recv(HEADER_SIZE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)

            # print(msg)
            
            msg = msg.split(" ")
            base_pos = int(msg[1])
            elbow_pos = int(msg[2])
            gripper_pos = msg[0]

            # print("Base position: ", base_pos)
            # print("Elbow position: ", elbow_pos)
    except Exception as e:
        running = False
        sleep(1)
        break
            
            
