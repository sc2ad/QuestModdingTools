import sys
import struct

def set_bytes(fileName, offset, bts):
    with open(fileName, "w+b") as fh:
        fh.seek(offset)
        print("Wrote: " + str(bts) + " to offset: " + str(hex(offset)))
        fh.write(bts)

def check(fileName, offset):
    print("VALIDATION:")
    with open(fileName, 'r+b') as f:
        f.seek(offset)
        print("Value 0: " + str(hex(struct.unpack('B', f.read(1))[0])))
        print("Value 1: " + str(hex(struct.unpack('B', f.read(1))[0])))
        print("Value 2: " + str(hex(struct.unpack('B', f.read(1))[0])))
        print("Value 3: " + str(hex(struct.unpack('B', f.read(1))[0])))

off = int(0x0109d074)

if __name__ == "__main__":
    set_bytes(sys.argv[1], off, bytes([0x01, 0x00, 0xa0, 0xe3]))

    check(sys.argv[1], off)
