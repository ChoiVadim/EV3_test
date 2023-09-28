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
motor_speed = 10
running = True

# Initialize motor states
elbow_motor_state = 0
base_motor_state = 0
gripper_motor_state = 0

# Initialize motor objects
class MotorThread(threading.Thread):
    def __init__(self):
        # Initialize the motors
        self.base_motor = LargeMotor(OUTPUT_A)
        self.elbow_motor = LargeMotor(OUTPUT_B)
        self.gripper_motor = MediumMotor(OUTPUT_C)
        threading.Thread.__init__(self)

    def run(self):
        try:
            while running:
                # Run the motors
                self.elbow_motor.on(speed=motor_speed*elbow_motor_state)
                self.base_motor.on(speed=motor_speed*base_motor_state)
                self.gripper_motor.on(speed=motor_speed*gripper_motor_state)
            # Stop the motors
            self.elbow_motor.stop()
            self.base_motor.stop()
            self.gripper_motor.stop()

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

        # Move the base motor
        if message == "Q":
            base_motor_state = -1
        if message == "E":
            base_motor_state = 1

        # Move the elbow motor
        if message == "R":
            elbow_motor_state = -1
        if message == "F":
            elbow_motor_state = 1

        # Move the gripper motor
        if message == "T":
            gripper_motor_state = -1
        if message == "G":
            gripper_motor_state = 1

        # Stop the motors when the key is released
        if message == "QES":
            base_motor_state = 0
        if message == "RFS":
            elbow_motor_state = 0
        if message == "TGS":
            gripper_motor_state = 0

        # Speed up and down
        if message == "SU":
            if motor_speed < 100:
                motor_speed += 5
        if message == "SD":
            if motor_speed > 5:
                motor_speed -= 5

        # Beep
        if message == "BEEP":
            sound.beep()

        # Stop the program
        if message == "Exit":
            running = False
            time.sleep(1)
            break

    # Close the client socket 
    client.close()
    time.sleep(1)

    
if __name__ == '__main__':
    main()