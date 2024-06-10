from network import Network
from time import sleep

NO_DEVICES = 3
CABLE_LENGTH = 50
MAX_ATEMPTS = 16


def main():
    network = Network(NO_DEVICES, CABLE_LENGTH, MAX_ATEMPTS)

    for _ in range(100):
        network.next_tick()
        sleep(0.01)

    network.show_statistics()

if __name__ == "__main__":
    main()