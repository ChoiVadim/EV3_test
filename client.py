import bluetooth

# Set up the Bluetooth connection
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

bluetooth.advertise_service(server_sock, "EV3Controller", service_id=bluetooth.SERIAL_PORT_CLASS, profiles=[bluetooth.SERIAL_PORT_PROFILE])

print(f"Waiting for connection on RFCOMM channel {port}")

client_sock, client_info = server_sock.accept()
print(f"Accepted connection from {client_info}")

# Remote control loop
while True:
    command = input("Enter command (e.g., 'forward', 'stop', 'exit'): ")
    client_sock.send(command.encode())

    if command == "exit":
        break

client_sock.close()
server_sock.close()