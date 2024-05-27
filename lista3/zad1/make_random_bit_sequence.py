import random


def make_sequence(file_name: str, n: int):
    with open(file_name, 'w') as file:
        for i in range(n):
            file.write(str(random.randint(0, 1)))