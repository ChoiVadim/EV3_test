import bluetooth
from ev3dev2.motor import LargeMotor, OUTPUT_A

# Set up the Bluetooth connection
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock.connect(("MAC_ADDRESS_OF_BRICK1", 1))  # Replace with Brick 1's MAC address

# Initialize motor
motor = LargeMotor(OUTPUT_A)

# Remote control loop
while True:
    received_command = client_sock.recv(1024).decode()

    if received_command == "forward":
        motor.on(50)
    elif received_command == "stop":
        motor.stop()
    elif received_command == "exit":
        break

motor.stop()
client_sock.close()