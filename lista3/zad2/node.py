class Node:
    def __init__(self):
        self.right_node : Node = None
        self.left_node : Node = None
        self.next_right_signal = []
        self.next_left_signal = []
        self.right_signal = []
        self.left_signal = []
        self.connection = []
    

    def get_collision_info(self):
        signals = self.left_signal + self.right_signal + self.connection
        return len(signals) >= 2
    

    def get_signal_info(self):
        signals = self.left_signal + self.right_signal + self.connection
        no_signals = len(signals)

        if no_signals == 0:
            return '_'
        elif no_signals == 1:
            return signals[0]
        elif '!' in signals:
            return '!'
        else:
            return '#'


    def propagate(self):
        if self.right_node != None:
            self.right_node.set_next_left_signal(self.left_signal + self.connection)
        if self.left_node != None:
            self.left_node.set_next_right_signal(self.right_signal + self.connection)


    def update(self):
        self.right_signal = self.next_right_signal
        self.left_signal = self.next_left_signal
        self.next_right_signal = []
        self.next_left_signal = []
        self.connection = []

    
    def set_next_right_signal(self, signal):
        self.next_right_signal = signal

    def set_next_left_signal(self, signal):
        self.next_left_signal = signal


    def set_right_node(self, node):
        self.right_node = node

    def set_left_node(self, node):
        self.left_node = node

    def set_connection(self, connection):
        self.connection = connection
