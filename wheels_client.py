#!/usr/bin/env python3

import socket 
from time import sleep
import threading

from ev3dev2.motor import LargeMotor 
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.sound import Sound


# Server MAC address
HOST = 'C0:3C:59:D8:CE:8E'
PORT = 5

# Define motor speeds
motor_speed = 20
running = True

# Initialize motor states
left_motor_state = 0
right_motor_state = 0

# Initialize motor objects
class MotorThread(threading.Thread):
    def __init__(self):
        # Initialize the motors
        self.left_motor = LargeMotor(OUTPUT_A)
        self.right_motor = LargeMotor(OUTPUT_B)
        threading.Thread.__init__(self)

    def run(self):
        try:
            while running:
                # Run the motors
                self.left_motor.on(speed=motor_speed*left_motor_state)
                self.right_motor.on(speed=motor_speed*right_motor_state)
            # Stop the motors
            self.left_motor.stop()
            self.right_motor.stop()

        except Exception as e:
            print("An error occurred:", str(e))


def main():    
    # Global variables because we need to modify them
    global left_motor_state
    global right_motor_state
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
    client.send("Wheels ready!".encode("ASCII"))

    # Play the sound
    sound = Sound()
    sound.speak('Wheels ready!')

    while True:
        # Receive message from the server
        message = client.recv(1024).decode("ASCII")

        # Move the robot
        if message == "W":
            right_motor_state = 1
            left_motor_state = 1
        if message == "S":
            right_motor_state = -1
            left_motor_state = -1
        if message == "A":
            right_motor_state = -1
            left_motor_state = 1
        if message == "D":
            right_motor_state = 1
            left_motor_state = -1

        # Stop the robot when the key is released
        if message == "WSS":
            right_motor_state = 0
            left_motor_state = 0
        if message == "ADS":
            right_motor_state = 0
            left_motor_state = 0

        # Speed up or down
        if message == "SU":
            if motor_speed < 100:
                motor_speed += 10
        if message == "SD":
            if motor_speed > 10:
                motor_speed -= 10

        # Beep
        if message == "BEEP":
            sound.beep()               

        # Stop the program
        if message == "Exit":
            running = False
            sleep(1)
            break

    # Close the client socket 
    client.close()
    sleep(1)

    
if __name__ == '__main__':
    main()