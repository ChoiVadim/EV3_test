#!/usr/bin/env python3

import socket 
from time import sleep
import threading

from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sound import Sound


# Server MAC address
HOST = 'C0:3C:59:D8:CE:8E'
PORT = 5

# Define motor speeds
motor_speed = 20
running = True

# Initialize motor states
elbow_motor_state = 0
base_motor_state = 0
gripper_motor_state = 0

# Initialize motor objects
class MotorThread(threading.Thread):
    def __init__(self):
        self.base_motor = LargeMotor(OUTPUT_A)
        self.elbow_motor = LargeMotor(OUTPUT_B)
        self.gripper_motor = MediumMotor(OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        try:
            while running:
                self.elbow_motor.on(speed=motor_speed*elbow_motor_state)
                self.base_motor.on(speed=motor_speed*base_motor_state)
                self.gripper_motor.on(speed=motor_speed*gripper_motor_state)
            self.elbow_motor.stop()
            self.base_motor.stop()
            self.gripper_motor.stop()
            print("Motors stopped.")

        except Exception as e:
            print("An error occurred:", str(e))


def main():
    # Global variables because we need to modify them
    global elbow_motor_state
    global base_motor_state
    global gripper_motor_state

    global motor_speed
    global running

    # Start the motor thread
    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()
    
    # Create the client socket and connect to the server
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect((HOST, PORT))

    # Send message to the server
    client.send("Arm ready!".encode("ASCII"))

    # Play the sound
    sound = Sound()
    sound.speak('Arm ready!')

    while True:
        # Receive the message from the server
        message = client.recv(1024).decode("ASCII")

        # Move the robot
        if message == '01000': # Forward
            elbow_motor_state = 1
        if message == '01100': # Backward
            elbow_motor_state = -1
        if message == '10000': # Turn left
            base_motor_state = -1
        if message == '10001': # Turn right
            base_motor_state = 1

        if message == '11001': # Open gripper
            gripper_motor_state = 1
        if message == '00000': # Close gripper
            gripper_motor_state = -1

        # Stop motors
        if message=='11111':
            elbow_motor_state = 0
            base_motor_state = 0
            gripper_motor_state = 0

    # Close the client socket 
    client.close()
    sleep(1)

    
if __name__ == '__main__':
    main()