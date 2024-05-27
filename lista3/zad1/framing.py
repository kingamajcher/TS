from crc import Calculator, Crc32
from random import randint

FLAG_SEQUENCE = '01111110'
FRAME_SIZE = 100
CRC_SIZE = 32

def adding_crc(string_of_bytes: str):
    calculator = Calculator(Crc32.CRC32)
    checkSum = calculator.checksum(bytes(string_of_bytes, 'utf-8'))
    crc_string = bin(checkSum)[2:].zfill(CRC_SIZE)

    return string_of_bytes + crc_string

def encode(input_file: str, output_file: str):
    with open(input_file, 'r') as file:
        input_stream = file.readline().strip()

    print(f"Input: {input_stream}\n")

    with open(output_file, 'w') as file:
        while len(input_stream) > 0:
            if len(input_stream) < FRAME_SIZE:
                bit_string = input_stream
                input_stream = ''
            else:
                bit_string = input_stream[:FRAME_SIZE]
                input_stream = input_stream[FRAME_SIZE:]

            print(f"Sequence:          {bit_string}")
            bit_string = adding_crc(bit_string)
            print(f"Sequence with CRC: {bit_string}")
            bit_string = replace(bit_string, '011111', '0111110')
            bit_string = FLAG_SEQUENCE + bit_string + FLAG_SEQUENCE
            file.write(bit_string + "\n")

            print(f"Frame: {bit_string} added to file.\n")

def decode(input_file, output_file):
    calculator = Calculator(Crc32.CRC32)
    with open(input_file, 'r') as file:
        input_stream = file.readlines()

    print(f"Input: {input_stream}\n")

    with open(output_file, 'w') as file:
        for bit_string in input_stream:
            bit_string = bit_string.strip()
            bit_string = bit_string.replace(FLAG_SEQUENCE, '')
            bit_string = replace(bit_string, '0111110', '011111')
            crc_string = bit_string[-CRC_SIZE:]
            bit_string = bit_string[:-CRC_SIZE]

            # verifying crc
            if calculator.verify(bytes(bit_string, 'utf-8'), int(crc_string, 2)):
                file.write(bit_string)
                print(f"CRC correct, sequence added to file: {bit_string}\n")
            else:
                print(f"CRC incorrect, sequence not added to file: {bit_string}\n")

def check(input_file, output_file):
    with open(input_file, 'r') as file:
        file1 = file.readline().strip()
    with open(output_file, 'r') as file:
        file2 = file.readline().strip()

    return file1 == file2

def change_bit(filename):
    with open(filename, 'r') as file:
        input_stream = file.readlines()

    x = randint(0, len(input_stream) - 1)
    y = randint(0, len(input_stream[x]) - 1)

    new_char = '1' if input_stream[x][y] == '0' else '0'
    input_stream[x] = input_stream[x][:y] + new_char + input_stream[x][y + 1:]

    with open(filename, 'w') as file:
        for bit_string in input_stream:
            file.write(bit_string)

def replace(text: str, target: str, replacement: str):
    for _ in range(3):
        text = text.replace(target, replacement)
    return text
