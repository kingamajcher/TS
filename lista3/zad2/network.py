from node import Node
from random import randint
from device import Device

NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Network:
    def __init__(self, no_devices, cable_length, max_atempts):
        self.device_name_index = 0
        self.cable_length = cable_length
        self.max_atempts = max_atempts
        self.max_wait_time = 7 * cable_length

        self.devices = []
        self.create_cable(cable_length)
        self.connect_devices(no_devices)

        self.log_file = open("network_log.txt", "w")


    def create_cable(self, cable_length):
        self.cable = [Node() for _ in range(cable_length)]

        # connecting pieces of cable
        for idx, elem in enumerate(self.cable):
            if idx == 0:
                prev_node = elem
                continue

            prev_node.set_right_node(elem)
            elem.set_left_node(prev_node)
            prev_node = elem
        

    def connect_devices(self, no_devices):
        while no_devices  >  0:
            if self.add_device(randint(0, self.cable_length - 1)):
                no_devices -= 1


    def add_device(self, distance):
        for device in self.devices:
            if device.distance == distance:
                return False

        name = NAMES[self.device_name_index]
        node = self.cable[distance]
        device = Device(name, node, distance, self.max_wait_time, self.max_atempts, 2 * self.cable_length)
        self.devices.append(device)
        self.device_name_index +=1

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
        for device in self.devices:
            print(device.get_message_data())

    def write_log(self, message):
        self.log_file.write(message)
