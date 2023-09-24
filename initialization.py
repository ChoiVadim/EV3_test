#!/usr/bin/env pybricks-micropython

from threading import Thread

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button

from pybricks.messaging import BluetoothMailboxServer, TextMailbox


# Initialize the EV3 Brick, Motor ABC and Touch Sensor, Color Sensor.
ev3 = EV3Brick()

gripper_motor = Motor(Port.A)
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# belt_motor = Motor(Port.D)

base_switch = TouchSensor(Port.S1)
elbow_sensor = ColorSensor(Port.S3)

def initialization():

    def initialize_base():
        base_motor.run(-60)
        while not base_switch.pressed():
            wait(10)
        base_motor.reset_angle(0)
        base_motor.hold()

    def initialize_elbow():
        elbow_motor.run_time(-30, 500)
        elbow_motor.run(15)
        while elbow_sensor.reflection() < 32:
            wait(10)
        elbow_motor.reset_angle(0)
        elbow_motor.hold()

    def initialize_gripper():
        gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
        gripper_motor.reset_angle(0)
        gripper_motor.run_target(200, -90)

    t1 = Thread(target=initialize_base).start()
    t2 = Thread(target=initialize_gripper).start()
    initialize_elbow()
  
    ev3.speaker.say("Initialization complete!")

def completion():
    base_motor.run_target(60, 0)
    elbow_motor.run_target(60, -30)
    gripper_motor.run_target(200, 0)

    ev3.speaker.say("Completion done!")

def robot_pick(position):
    # Rotate to the pick-up position.
    base_motor.run_target(200, position)
    # Lower the arm.
    elbow_motor.run_target(60, -55)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(60, 0)

def robot_release(position):
    # Rotate to the drop-off position.
    base_motor.run_target(200, position)
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(60, -55)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -90)
    # Raise the arm.
    elbow_motor.run_target(60, 0)

def throw_ball():

    base_motor.run_target(60, 25)
    elbow_motor.run_target(60, -30)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    
    Thread(target=elbow_motor.run_target, args=(300, 0)).start()
    Thread(target=base_motor.run_target, args=(300, 90)).start()
    wait(300)
    gripper_motor.run_target(250, -90)

    wait(500)
    base_motor.run_target(60, 0)

    belt_motor.run_target(60, -205)
    belt_motor.reset_angle(0)


def main():
    initialization()
    while ev3.buttons.pressed() != [Button.CENTER]:
        if ev3.buttons.pressed() == [Button.RIGHT]:
            throw_ball()
    completion()


if __name__  == "__main__":
    main()                               
    
