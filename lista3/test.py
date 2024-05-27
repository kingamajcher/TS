from framing import encode, decode, change_bit, check
from make_random_bit_sequence import make_sequence

INPUT_FILE = "Z.txt"
OUTPUT_FILE = "W.txt"
DECODED_FILE = "Z_decoded.txt"

def test_framing():
    print("FRAMING")
    make_sequence(INPUT_FILE, 500)
    encode(INPUT_FILE, OUTPUT_FILE)

    print("DECODING")
    decode(OUTPUT_FILE, DECODED_FILE)
    print(check(INPUT_FILE, DECODED_FILE))

def test_framing_with_wrong_byte():
    print("FRAMING")
    make_sequence(INPUT_FILE, 500)
    encode(INPUT_FILE, OUTPUT_FILE)

    print("Changed random bit")
    change_bit(OUTPUT_FILE)

    print("DECODING")
    decode(OUTPUT_FILE, DECODED_FILE)
    print(check(INPUT_FILE, DECODED_FILE))
    

def main():
    test_framing()
    # test_framing_with_wrong_byte()

if __name__ == "__main__":
    main()
