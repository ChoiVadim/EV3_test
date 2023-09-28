import socket 
import keyboard
from time import sleep


# The MAC address of a Bluetooth adapter on the server
HOST = 'C0:3C:59:D8:CE:8E'
# The port used by the server
PORT = 5

ARM_SPEED = 10
WHEELS_SPEED = 20

def main():
    global ARM_SPEED
    global WHEELS_SPEED

    # Create the server socket
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind((HOST, PORT))
    server.listen(2)

    # Accept connections from the first client
    robot_arm_socket, address = server.accept()
    print('Connected by ', address)
    message = robot_arm_socket.recv(1024).decode("utf-8")
    print('Received message: ', message)

    # Accept connections from the second client
    wheels_socket, address2 = server.accept()
    print('Connected by ', address2)
    message = wheels_socket.recv(1024).decode("utf-8")
    print('Received message: ', message)

    # Send commands to the client
    while True:
        event = keyboard.read_event()

        # Key press event
        if event.event_type == keyboard.KEY_DOWN:

            # Wheels
            if event.name == 'W':
                wheels_socket.send("W".encode("ASCII"))
            if event.name == 'S':
                wheels_socket.send("S".encode("ASCII"))
            if event.name == 'A':
                wheels_socket.send("A".encode("ASCII"))
            if event.name == 'D':
                wheels_socket.send("D".encode("ASCII"))

            # Robot arm
            if event.name == 'Q':
                robot_arm_socket.send("Q".encode("ASCII"))
            if event.name == 'E':
                robot_arm_socket.send("E".encode("ASCII"))
            if event.name == 'R':
                robot_arm_socket.send("R".encode("ASCII"))
            if event.name == 'F':
                robot_arm_socket.send("F".encode("ASCII"))
            if event.name == 'T':
                robot_arm_socket.send("T".encode("ASCII"))
            if event.name == 'G':
                robot_arm_socket.send("G".encode("ASCII"))
            
            # Speed up for wheels
            if event.name == 'up':
                if WHEELS_SPEED < 100:
                    WHEELS_SPEED += 10
                    print("Wheels speed: ", WHEELS_SPEED)
                    wheels_socket.send("SU".encode("ASCII"))
            if event.name == 'down':
                if WHEELS_SPEED > 10:
                    WHEELS_SPEED -= 10
                    print("Wheels speed: ", WHEELS_SPEED)
                    wheels_socket.send("SD".encode("ASCII"))

            # Speed up for robot arm
            if event.name == 'right':
                if ARM_SPEED < 100:
                    ARM_SPEED += 5
                    print("Arm speed: ", ARM_SPEED)
                    robot_arm_socket.send("SU".encode("ASCII"))
            if event.name == 'left':
                if ARM_SPEED > 5:
                    ARM_SPEED -= 5
                    print("Arm speed: ", ARM_SPEED)
                    robot_arm_socket.send("SD".encode("ASCII"))

            # Beep
            if event.name == 'space':
                robot_arm_socket.send("BEEP".encode("ASCII"))
                wheels_socket.send("BEEP".encode("ASCII"))

            # Exit
            if event.name == 'esc':
                robot_arm_socket.send("Exit".encode("ASCII"))
                wheels_socket.send("Exit".encode("ASCII"))
                break

        # Key release event
        if event.event_type == keyboard.KEY_UP:
            if event.name == 'W' or event.name == 'S':
                wheels_socket.send("WSS".encode("ASCII"))
            if event.name == 'A' or event.name == 'D':
                wheels_socket.send("ADS".encode("ASCII"))

            if event.name == 'Q' or event.name == 'E':
                robot_arm_socket.send("QES".encode("ASCII"))
            if event.name == 'R' or event.name == 'F':
                robot_arm_socket.send("RFS".encode("ASCII"))
            if event.name == 'T' or event.name == 'G':
                robot_arm_socket.send("TGS".encode("ASCII"))

    # Close the client socket
    robot_arm_socket.close()
    wheels_socket.close()
    sleep(1)


if __name__ == '__main__':
    main()