import socket


class DataSender:
    def __init__(self,
                 origin_ip,
                 destination_ip,
                 ttl,
                 tos):
        self.host = '127.0.0.1'
        self.port = 12345
        self.origin_ip = origin_ip
        self.destination_ip = destination_ip
        self.ttl = ttl
        self.tos = tos

    def send_data(self):
        with socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM) as interface:
            interface.connect((self.host, self.port))
            data = f"Data:{self.origin_ip}, {self.destination_ip}, {self.ttl}, {self.tos}".encode()
            interface.sendall(data)

            # Receives the response from the simulated router
            response = interface.recv(1024)

            # Displays the response on the screen
            print(response.decode())


if __name__ == '__main__':
    sender = DataSender('192.168.0.1', '192.168.0.2', 5, 1)
    sender.send_data()
