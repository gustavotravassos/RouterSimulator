import socket
import time
import threading


class NetworkInterface:
    def __init__(self,
                 router_name,
                 destination_network,
                 output_interface):

        self.router_name = router_name
        self.destination_network = destination_network
        self.output_interface = output_interface
        self.distance = 0
        self.next_hop = None

        self.routing_table = {self.router_name: {'destination_network': self.destination_network,
                                                 'output_interface': self.output_interface,
                                                 'distance': self.distance,
                                                 'next_hop': self.next_hop}}

        self.host = '127.0.0.1'
        self.port = 12345

        self.interface = socket.socket(socket.AF_INET,
                                       socket.SOCK_STREAM)

        self.interface.connect((self.host,
                                self.port))

    def add_neighbor_router(self, neighbor_router, destination_network, output_interface, distance):
        self.routing_table[neighbor_router.name] = {'destination_network': destination_network,
                                                    'output_interface': output_interface,
                                                    'distance': distance,
                                                    'next_hop': neighbor_router}

    def send_routing_package(self):
        while True:
            # TODO: Melhorar esse print para ter as informações passadas
            print(
                f"Routing Package: " + f"{self.router_name}, {self.destination_network}, {self.output_interface}, {self.distance}, {self.next_hop}")
            package = f"Routing:{self.router_name}, {self.destination_network}, {self.output_interface}, {self.distance}, {self.next_hop}".encode()
            self.interface.sendall(package)
            time.sleep(300)

    def receive_routing_package(self):
        while True:
            received_package = self.interface.recv(1024)
            # print(f"------------ New package ------------")
            # print(f"{self.router_name}")
            print(f"Received package containing: {received_package.decode()}")

    def __del__(self):
        self.interface.close()


if __name__ == '__main__':
    routers = [
        NetworkInterface("Router 1",
                         "192.168.0.1",
                         "Interface 1"),
        NetworkInterface("Router 2",
                         "192.168.0.2",
                         "Interface 2"),
        NetworkInterface("Router 3",
                         "192.168.0.3",
                         "Interface 3"),
        NetworkInterface("Router 4",
                         "192.168.0.4",
                         "Interface 4")
    ]

    sender_threads = []
    receiver_threads = []

    for router in routers:
        sender = threading.Thread(target=router.send_routing_package)
        sender.start()
        sender_threads.append(sender)

    for router in routers:
        receiver = threading.Thread(target=router.receive_routing_package)
        receiver.start()
        receiver_threads.append(receiver)

    for sender in sender_threads:
        sender.join()

    for receiver in receiver_threads:
        receiver.join()
