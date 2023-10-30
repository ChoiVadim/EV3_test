#!/usr/bin/env python3

import socket
import threading
from time import sleep

from ev3dev2.sound import Sound
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

# Variables for the motors
base_pos = 0
elbow_pos = 0
gripper_pos = ''
running = True
motor_speed = 10
# The difference between the current and desired position
diff_between_pos = 20 


class MotorThread(threading.Thread):
    def __init__(self):
        self.base_motor = LargeMotor(OUTPUT_A)
        self.elbow_motor = LargeMotor(OUTPUT_B)
        self.gripper_motor = MediumMotor(OUTPUT_C)
        threading.Thread.__init__(self)

    def stop(self):
        self.base_motor.stop()
        self.elbow_motor.stop()
        self.gripper_motor.stop()
        self.base_motor.on_to_position(speed=10, position=0)
        self.elbow_motor.on_to_position(speed=10, position=0)
        self.gripper_motor.on_to_position(speed=10, position=0)

        print("Motors stopped.")

    def run(self):
        try:
            self.base_motor.reset()
            self.elbow_motor.reset()
            self.gripper_motor.reset()
             
            while running:
                # Move the motors to the desired positions.
                # If the difference between the current and desired
                # position is greater than x, move the motor. 
                # Otherwise, stop the motor

                # Get the current motor positions
                current_b_pos = self.base_motor.position
                current_e_pos = self.elbow_motor.position
                current_g_pos = self.gripper_motor.position 

                # Base motor
                if abs(current_b_pos - base_pos) > diff_between_pos:
                    if current_b_pos < base_pos:
                        self.base_motor.on(speed=motor_speed) # Go left
                    if current_b_pos > base_pos:
                        self.base_motor.on(speed=-motor_speed) # Go right
                else:
                    self.base_motor.stop()
                
                # Elbow motor
                if abs(elbow_pos - current_e_pos) > diff_between_pos:
                    if elbow_pos > current_e_pos:
                        self.elbow_motor.on(speed=motor_speed) # Go down
                    if elbow_pos < current_e_pos:
                        self.elbow_motor.on(speed=-motor_speed) # Go up
                else:
                    self.elbow_motor.stop()

                # Gripper motor
                if gripper_pos == '00000':
                    self.gripper_motor.on(speed=20) # Close
                    if current_g_pos > 40:
                        self.gripper_motor.stop()
                if gripper_pos == '11111':
                    self.gripper_motor.on(speed=-20) # Open
                    if current_g_pos <= 0:
                        self.gripper_motor.stop()
                
            # if running is False stop all motors and reset them
            self.stop()

        except Exception as e:
            self.stop()
            # Stop all motors and reset them if an error occurs
            print("An error occurred:", str(e))


def main():
    # Global variables because we need to modify them
    global base_pos
    global elbow_pos
    global gripper_pos
    global motor_speed
    global running
    global diff_between_pos
        
    # Create the client socket and connect to the server
    client = socket.socket(socket.AF_BLUETOOTH,
                            socket.SOCK_STREAM,socket.BTPROTO_RFCOMM)
    client.connect((HOST, PORT))

    # Send message to the server
    client.send("Arm ready!".encode("ASCII"))

    # Create the motor thread and start it
    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()

    # Play the sound
    sound = Sound()
    sound.speak('Wheels ready!')

    # Main loop receiving messages from the server and changing the motor positions
    while True:
        try:
            # Receive message from the server
            msg_length = client.recv(HEADER_SIZE).decode(FORMAT)

            # If the message is not empty, decode it
            if msg_length:
                # Get the message length
                msg_length = int(msg_length)
                # Get the message with the given length
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)

                # Split the message into the base, elbow and gripper positions
                msg = msg.split(" ")
                base_pos = int(msg[1])
                elbow_pos = int(msg[2])
                gripper_pos = msg[0]

                # Change the motor speed
                if msg[0] == '11001':
                    motor_speed = 60
                    diff_between_pos = 40
                if msg[0] == '10001':
                    motor_speed = 10


        except Exception as e:
            # If an error occurs, stop the motor thread and close the client socket
            running = False
            client.close()
            break

    # Close the client socket 
    print("Closing the client socket...")
    client.close()
    sleep(1)
        
            
if __name__ == '__main__':
    main()