import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.16"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            this = [self.client.recv(2048*5), int(self.client.recv(2048*5).decode('utf-8'))]
            return this
           
        except:
            pass

    def send(self, data):
        #x, y, bulletx, bullety, facing
        try:
            print(bytes(f'({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]})', 'utf-8'), 'this is what being sent to server')
            self.client.send(bytes(f'({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]})', 'utf-8'))
            return self.client.recv(2048*5).decode('utf-8')
        except socket.error as e:
            print(e)