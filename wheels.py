#!/usr/bin/env python3

import socket 
from time import sleep
import threading

from ev3dev2.motor import LargeMotor 
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.sound import Sound


# The MAC address of a Bluetooth adapter on the server
HOST = 'C0:3C:59:D8:CE:8E'
# The port used by the server
PORT = 6
# The size of the header
HEADER_SIZE = 64
# The format of the message
FORMAT = "ASCII"

# Define motor speeds
motor_speed = 40
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
            self.left_motor.stop()
            self.right_motor.stop()
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
    client.send("Wheels ready!".encode(FORMAT))

    # Play the sound
    sound = Sound()
    sound.speak('Wheels ready!')

    while True:
        try:
            # Receive message from the server
            message = client.recv(HEADER_SIZE).decode(FORMAT)

            # Move the robot
            if message == '01000': # Forward
                right_motor_state = -1
                left_motor_state = -1
            if message == '01100': # Backward
                right_motor_state = 1
                left_motor_state = 1
            if message == '10001': # Turn left
                right_motor_state = -1
                left_motor_state = 1
            if message == '10000': # Turn right
                right_motor_state = 1
                left_motor_state = -1

            # Stop motors
            if message=='11111':
                right_motor_state = 0
                left_motor_state = 0

            # Change motor speed
            if message == '11000':
                motor_speed = 10
            if message == '11100':
                motor_speed = 40

            if message == '11001':
                motor_speed = 100
                right_motor_state = -1
                left_motor_state = 1 
                

        except Exception as e:
            running = False
            print("An error occurred:", str(e))
            break
        
    # Close the client socket 
    print("Closing connection...")
    client.close()
    sleep(1)

    
if __name__ == '__main__':
    main()