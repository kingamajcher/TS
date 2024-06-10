from node import Node
from random import randint
from device import Device

NAMES = "ABCDEFGHIJKL"


class Network:
    def __init__(self, no_devices, cable_length, max_atempts, left_margin = 0, right_margin = 0):
        self.device_name_ind = 0
        self.cable_length = cable_length + left_margin + right_margin
        self.max_atempts = max_atempts
        self.max_wait_time = 7 * cable_length

        self.devices = []
        self.create_cable(cable_length, left_margin + right_margin)
        self.connect_devices(no_devices, left_margin, right_margin)

        self.log_file = open("network_log.txt", "w")



    def create_cable(self, cable_length, cable_margin):
        self.cable = [Node() for _ in range(cable_length + cable_margin)]

        #Connect pieces of cable
        for ind, elem in enumerate(self.cable):
            if ind == 0:
                prev_node = elem
                continue

            prev_node.set_right_node(elem)
            elem.set_left_node(prev_node)
            prev_node = elem
        

    def connect_devices(self, no_devices: int, left_margin: int, right_margin: int) -> None:
        self.add_device(left_margin)
        
        self.add_device(self.cable_length - right_margin - 1)

        while no_devices - 2  >  0:
            if self.add_device(randint(left_margin, self.cable_length - right_margin - 1)):
                no_devices -= 1


    def add_device(self, distance):
        for comp in self.devices:
            if comp.distance == distance:
                return False

        name = NAMES[self.device_name_ind]
        node = self.cable[distance]
        device = Device(name, node, distance, self.max_wait_time, self.max_atempts, 2 * self.cable_length)
        self.devices.append(device)
        self.device_name_ind +=1

        return True
    

    def next_tick(self):
        for node in self.cable:
            node.propagate()

        for node in self.cable:
            node.update()
        
        for device in self.devices:
            device.run()

        self.show_network()


    def get_signals(self):
        return "".join(node.get_signal_info() for node in self.cable)
        
    def show_network(self):
        signals = self.get_signals()

        print(signals)
        self.write_log(signals + "\n")
    
    
    def show_statistics(self):
        print()
        for comp in self.devices:
            print(comp.get_message_data())

    def write_log(self, message):
        self.log_file.write(message)
