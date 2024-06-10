from random import randint, random

class Device:
    def __init__(self, name, node, distance, max_wait_time, max_atempts, min_message_length):
        self.name = name
        self.node = node
        self.distance = distance
        self.max_atempts = max_atempts
        self.max_wait_time = max_wait_time
        self.min_message_length = min_message_length

        self.no_atempts = 0
        self.no_successes = 0
        self.no_messages = 0
        
        self.jam_time = 0
        self.message_time = 0
        self.waiting_time = 0
        self.initial_message_time = 0
        self.empty_cable_waiting_time = 0
        
        
        self.transmiting = False
        self.queued_message = False
        
        self.log = ""

        self.set_message_chance()
        self.short_wait()
    

    def run(self):
        if self.jam_time > 0: # sending jam signal
            self.node.set_connection(['!'])
            self.jam_time -= 1

        elif self.queued_message == False: # queuing message
            self.queue_message()
    
        elif self.waiting_time > 0: # waiting for transmission
            self.waiting_time -= 1
        

        elif self.message_time == 0: # succesfuly transmiting message
            self.queued_message = False
            self.no_successes += 1
            
            self.long_wait()
            self.set_message_chance()
        
        elif self.no_atempts >= self.max_atempts: # failing to transmit message
            self.queued_message = False
            
            self.short_wait()
            self.set_message_chance()

        else: # sending message
            self.send_message()



    def queue_message(self, now = False): # queuing message
        if random() > self.message_chance and not now:
            return

        self.initial_message_time = randint(self.min_message_length, self.min_message_length * 1.5)
        self.message_time = self.initial_message_time
        self.queued_message = True
        self.no_messages += 1
        self.no_atempts = 0
    

    def send_message(self): # sending message
        if self.transmiting:
            self.node.set_connection([self.name])

            if self.node.get_collision_info(): # collision
                self.transmiting = False
                self.no_atempts += 1
                self.waiting_time = randint(self.max_wait_time // 2, self.max_wait_time)
                self.message_time = self.initial_message_time
                
                self.jam_time = 5
                self.short_wait()

            else: # sent successfully
                self.message_time -= 1

        elif self.node.get_signal_info ==  '!': # jam
            if self.short_wait == 0:
                self.short_wait()


        elif self.node.get_signal_info() != '_': # cable is occupied
            if self.empty_cable_waiting_time == 0:
                self.empty_cable_waiting_time = randint(self.max_wait_time // 8, self.max_wait_time // 4)
        
        elif self.empty_cable_waiting_time == 0: # cable is empty, starting transmission
            self.transmiting = True
        
        else:
            self.empty_cable_waiting_time -= 1        
        

    def get_message_data(self):
        success_rate = self.no_successes / max(self.no_messages - 1, 1) * 100
        return f"Messages: {max(self.no_messages - 1, 0):4}    Successes: {self.no_successes:4}    Success rate: {success_rate:7.2f}%"
    
    def short_wait(self):
        self.waiting_time = randint(1,  self.max_wait_time // 2)

    def long_wait(self):
        self.waiting_time = randint(self.max_wait_time // 2, self.max_wait_time)

    def set_message_chance(self):
        self.message_chance = 1.0 / randint(4, 16)