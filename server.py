import socket 
import keyboard

# hcitool dev | cut -sf3
# HOST = '00:17:E9:F9:07:CC'
HOST = 'C0:3C:59:D8:CE:8E'
PORT = 5

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((HOST, PORT))

server.listen(2)

robot_arm_socket, address = server.accept()
print('Connected by ', address)
message = robot_arm_socket.recv(1024).decode("utf-8")
print('Received message: ', message)

wheels_socket, address2 = server.accept()
print('Connected by ', address2)
message = wheels_socket.recv(1024).decode("utf-8")
print('Received message: ', message)

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'space':
            print('You pressed space!')
            robot_arm_socket.send("Run".encode("utf-8"))
    if event.event_type == keyboard.KEY_UP:
        if event.name == 'space':
            wheels_socket.send("Run".encode("utf-8"))
    if event.event_type == keyboard.KEY_DOWN and event.name == "esc":
        break
robot_arm_socket.close()
wheels_socket.close()

    