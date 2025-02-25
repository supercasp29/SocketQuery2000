import socket
import uuid
import threading
import signal
import sys
import select

server_id = str(uuid.uuid4())
clients = set()

HOST, PORT = "0.0.0.0", 9999

def process_command(command):
    if command == "WHO":
        return str(len(clients))
    elif command == "WHERE":
        return server_id
    elif command == "WHY":
        return "42"
    else:
        return "ERROR: Unknown Command"

def handle_client(conn, addr):
    print(f"New connection from {addr}", flush=True)
    clients.add(conn)
    try:
        while True:
            # Use select to wait for data to be available for reading
            readable, _, _ = select.select([conn], [], [], 0.1)
            if conn in readable:
                try:
                    data = conn.recv(1024).strip()
                    if not data:
                        break
                    print(f"Received data: {data}", flush=True)  # Debugging line
                    command = data.decode('ascii').upper()
                    response = process_command(command)
                    print(f"Sending response: {response}", flush=True)  # Debugging line
                    conn.sendall(response.encode('ascii'))
                except BlockingIOError:
                    # This exception can be ignored as select ensures readiness
                    pass
    finally:
        clients.remove(conn)
        conn.close()

def signal_handler(sig, frame):
    print("Shutting down server...", flush=True)
    server.close()
    sys.exit(0)


# Handle SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
server.setblocking(False)  # Set the server socket to non-blocking mode
print(f"Server started on {HOST}:{PORT}", flush=True)

# Use select to handle multiple connections without blocking
while True:
    try:
        # Check for readable sockets
        readable, _, _ = select.select([server], [], [], 0.1)
        
        for s in readable:
            if s is server:
                conn, addr = server.accept()
                conn.setblocking(False)  # Set each client socket to non-blocking
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
                
    except KeyboardInterrupt:
        # Graceful shutdown when Ctrl+C is pressed
        print("Shutting down server...", flush=True)
        server.close()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", flush=True)
