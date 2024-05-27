from framing import encode, decode, change_bit, check
from make_random_bit_sequence import make_sequence

INPUT_FILE = "Z.txt"
OUTPUT_FILE = "W.txt"
DECODED_FILE = "Z_decoded.txt"

def test_framing():
    print("FRAMING")
    make_sequence(INPUT_FILE, 500)
    encode(INPUT_FILE, OUTPUT_FILE)

    print("DECODING unchanged sequence")
    decode(OUTPUT_FILE, DECODED_FILE)
    if check(INPUT_FILE, DECODED_FILE) == True:
        print("decoded correctly :)")
    else:
        print("decoding failed :(")

def test_framing_with_wrong_byte():
    print("FRAMING")
    make_sequence(INPUT_FILE, 500)
    encode(INPUT_FILE, OUTPUT_FILE)

    print("Changed random bit \n")
    change_bit(OUTPUT_FILE)

    print("DECODING changed sequence")
    decode(OUTPUT_FILE, DECODED_FILE)
    if check(INPUT_FILE, DECODED_FILE) == True:
        print("decoded correctly :)")
    else:
        print("decoding failed :(")
    

def main():
    test_framing()
    print('\n')
    test_framing_with_wrong_byte()

if __name__ == "__main__":
    main()
