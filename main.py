#!/usr/bin/env python3

import time
import evdev
from evdev import InputDevice
from evdev import ecodes as e
import threading

from ev3dev2.motor import LargeMotor, MediumMotor 
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sound import Sound


# Define motor speeds
motor_speed = 20
running = True

# Initialize motor states
elbow_motor_state = 0
base_motor_state = 0
gripper_motor_state = 0
belt_motor_state = 0

# Initialize motor objects
class MotorThread(threading.Thread):
    def __init__(self):
        self.base_motor = LargeMotor(OUTPUT_A)
        self.elbow_motor = LargeMotor(OUTPUT_B)
        self.gripper_motor = MediumMotor(OUTPUT_C)
        self.belt_motor = LargeMotor(OUTPUT_D)
        threading.Thread.__init__(self)

    def run(self):
        try:
            while running:
                self.elbow_motor.on(speed=motor_speed*elbow_motor_state)
                self.base_motor.on(speed=motor_speed*base_motor_state)
                self.gripper_motor.on(speed=motor_speed*gripper_motor_state)
                self.belt_motor.on(speed=motor_speed*belt_motor_state)
            self.elbow_motor.stop()
            self.base_motor.stop()
            self.gripper_motor.stop()
            self.belt_motor.stop()
            print("Motors stopped.")

        except Exception as e:
            print("An error occurred:", str(e))

def main():
    # Define the keyboard device path
    keyboard_device_path = "/dev/input/event2"
    # Initialize the keyboard device
    keyboard = InputDevice(keyboard_device_path)

    # Define key codes for controlling 
    keycode_elbow_up = e.KEY_W
    keycode_elbow_down = e.KEY_S
    keycode_base_left = e.KEY_A
    keycode_base_right = e.KEY_D
    keycode_grab = e.KEY_E
    keycode_release = e.KEY_SPACE
    keycode_belt_left = e.KEY_G
    keycode_belt_right = e.KEY_F
    keycode_stop = e.KEY_ESC

    # Global variables because we need to modify them
    global elbow_motor_state
    global base_motor_state
    global gripper_motor_state
    global belt_motor_state
    global running

    # Play the sound
    # sound = Sound()
    # sound.speak('Welcome to the E V 3 dev project!')
    print("Press ESC key to stop the program.")

    # Start the motor thread
    motor_thread = MotorThread()
    motor_thread.setDaemon(True)
    motor_thread.start()

    # Control the motors based on key presses
    for event in keyboard.read_loop():
        if event.type == evdev.ecodes.EV_KEY: 
            if event.value == 1:  # Key press event
                if event.code == keycode_elbow_down: elbow_motor_state = 1 
                if event.code == keycode_elbow_up: elbow_motor_state = -1

                if event.code == keycode_base_left: base_motor_state = 1
                if event.code == keycode_base_right: base_motor_state = -1

                if event.code == keycode_grab: gripper_motor_state = 1
                if event.code == keycode_release: gripper_motor_state = -1

                if event.code == keycode_belt_left: belt_motor_state = 1
                if event.code == keycode_belt_right: belt_motor_state = -1

                if event.code == keycode_stop:
                    print("Stopping the program...")
                    running = False
                    time.sleep(1)
                    break

            elif event.value == 0:  # Key release event
                if (event.code == keycode_elbow_up 
                    or event.code == keycode_elbow_down):
                    elbow_motor_state = 0
                if (event.code == keycode_base_left
                    or event.code == keycode_base_right):
                    base_motor_state = 0
                if (event.code == keycode_grab
                    or event.code == keycode_release):
                    gripper_motor_state = 0
                if (event.code == keycode_belt_left
                    or event.code == keycode_belt_right):
                    belt_motor_state = 0


if __name__ == "__main__":
    main()