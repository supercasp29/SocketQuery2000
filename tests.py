import socket

# Server address and port
HOST = "127.0.0.1"
PORT = 9999

# Function to send a command to the server and get a response
def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode('ascii') + b'\n')  # Send the command with a newline
        response = s.recv(1024).decode('ascii').strip()  # Receive the response and strip any extra spaces
    return response

# Test WHO command
response = send_command("WHO")
print(f"Response to WHO command: {response}")
assert response.isdigit(), "Response to WHO should be a number"
assert response == "1", "Expected response for WHO to be '1'"

# Test WHERE command
response = send_command("WHERE")
print(f"Response to WHERE command: {response}")
assert len(response) > 0, "Response to WHERE should not be empty"
assert all(c in "0123456789abcdef-" for c in response.lower()), "Response to WHERE should be a valid UUID"

# Test WHY command
response = send_command("WHY")
print(f"Response to WHY command: {response}")
assert response == "42", "Expected response for WHY to be '42'"

# Test UNKNOWN command
response = send_command("UNKNOWN")
print(f"Response to UNKNOWN command: {response}")
assert response == "ERROR: Unknown Command", "Expected response for unknown command to be 'ERROR: Unknown Command'"

print("All tests passed!")
