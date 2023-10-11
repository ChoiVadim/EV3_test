def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    msg_from_client = conn.recv(HEADER_SIZE).decode(FORMAT)
    print(f"[{addr}] {msg_from_client}")

    while connected:
        try:
            if MESSAGE:
                conn.send(MESSAGE.encode(FORMAT))

        except ConnectionAbortedError:
            print("Connection aborted")
            connected = False
            conn.close()


def start_server():
    print("Starting server...")
    # Create the server socket
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server is listening on {HOST}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Active connections: ", threading.activeCount() - 1)