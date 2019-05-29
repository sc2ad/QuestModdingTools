import sys
import struct

def set_bytes(fileName, offset, bts):
    with open(fileName, "r+b") as fh:
        fh.seek(offset - 4)
        print("Area Bytes:\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))
        print("\t\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))
        print("\t\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))
        fh.seek(offset)
        print("Wrote: " + str(bts.hex()) + " to offset: " + str(offset) + " replacing: " + str(fh.peek()[:len(bts)].hex()))
        fh.write(bts)

def check(fileName, offset):
    print("VALIDATION:")
    with open(fileName, 'rb') as fh:
        fh.seek(offset - 4)
        print("Area Bytes:\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))
        print("\t\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))
        print("\t\t\t" + " ".join([str(fh.read(1).hex()) for _ in range(4)]))

off = 0x0109d074

# Looking for:
# 06 00 00 1a 
# 01 00 a0 e3 
# 00 00 9f e7 

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Provide the directory to libil2cpp.so!")
    else:
        set_bytes(sys.argv[1], off, bytes([0x01, 0x00, 0xa0, 0xe3]))
        check(sys.argv[1], off)
    
