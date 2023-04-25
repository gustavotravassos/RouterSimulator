class Router:
    def __init__(self,
                 router_name):
        self.router_name = router_name
        self.routing_table = {self.router_name: {'destination_network': '192.168.0.5',
                                                 'output_interface': 0,
                                                 'distance': 0,
                                                 'next_hop': None}}

    def add_neighbor_router(self, neighbor_router, destination_network, output_interface, distance):
        self.routing_table[neighbor_router.router_name] = {'destination_network': destination_network,
                                                           'output_interface': output_interface,
                                                           'distance': distance,
                                                           'next_hop': neighbor_router}

    def update_routing_table(self, router, destination_network, output_interface, distance):
        if router.router_name not in self.routing_table or self.routing_table[router.router_name]['distance'] > distance:
            self.routing_table[router.router_name] = {'destination_network': destination_network,
                                                      'output_interface': output_interface,
                                                      'distance': distance,
                                                      'next_hop': router}

            for neighbor in self.routing_table:
                if neighbor != self.router_name and neighbor != router.router_name and neighbor in router.routing_table:
                    if self.routing_table[neighbor]['distance'] > self.routing_table[router.router_name]['distance'] + \
                            router.routing_table[neighbor]['distance']:
                        self.routing_table[neighbor] = {'destination_network': destination_network,
                                                        'output_interface': output_interface,
                                                        'distance': self.routing_table[router.router_name]['distance'] + router.routing_table[neighbor]['distance'],
                                                        'next_hop': router}

    def print_table(self):
        print(f"| Routing table for router {self.router_name} |")
        for line in self.routing_table:
            print(f"| {'-'*30} |")
            print(f"| Destination: {self.routing_table[line]['destination_network']} |")
            print(f"| Output Interface: {self.routing_table[line]['output_interface']} |")
            print(f"| Distance: {self.routing_table[line]['distance']} |")
            print(f"| Next Hop: {self.routing_table[line]['next_hop']} |")
            print(f"| {'-' * 30} |")

    def send_package(self, source_ip, destination_ip, ttl, tos):
        if source_ip not in self.routing_table:
            return f"Source IP address {source_ip} not found in the routing table"
        else:
            output_interface = self.routing_table[destination_ip]['output_interface']
            return f"Sending packet from {source_ip} to {destination_ip} via {output_interface}. TTL={ttl}, TOS={tos}"

    def handle_connection(self, connection, address):
        print(f"Connected to address: {address}")
        while True:
            content = connection.recv(1024)

            if not content:
                print("No package received, aborting")
                break

            print("Package received!")
            package_type, content = content.decode().split(':')

            if package_type == "Routing":
                print("Package Type: Routing")
                router_name, destination_network, output_interface, distance, next_hop = content.split(', ')
                # self.print_table()
                # self.update_routing_table(router_name, destination_network, output_interface, distance)

            elif package_type == "Data":
                print("Package Type: Data")
                source_ip, destination_ip, ttl, tos = content.split(', ')

                # response = self.send_package(source_ip, destination_ip, int(ttl), int(tos))

                # table_line = self.routing_table.get(destination_ip)

                # if table_line is not None:
                #     destination_connection = table_line['connection']
                #     destination_connection.sendall(response.encode())

                # else:
                #     print("There is no table_line for", destination_ip)

        connection.close()
