import argparse

def readData(fs, offset, length):
    fs.seek(offset)
    return fs.read(length)

def writeDataOffset(fs, offset, data):
    # Doesn't handle insertions.
    fs.seek(offset)
    fs.write(data)

def writeData(fs, data):
    fs.write(data)

def replaceData(fs, offset, oldLength, data):
    fs.seek(offset)
    # This is going to cause many problems with things that rely on the resource they want being at the offset they say
    # Perhaps it would make more sense to just insert at the end of the file (but then it still becomes challenging, just not nearly as hard)
    # TODO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Handles reading and writing of resource data at offsets.")
    parser.add_argument("resourceFile", type=str, help="Resource file to read/write from.")
    parser.add_argument("offset", type=int, help="The offset at which to read/write from.")
    parser.add_argument("length", type=int, help="The length at which to read/write until.")
    parser.add_argument("--load", type=str, help="The binary file to write in.")
    parser.add_argument("--output", type=str, help="The binary file to write the read response to.")

    args = parser.parse_args()

    with open(args.resourceFile, 'r+b') as fs:
        if args.load:
            with open(args.load, 'rb') as f:
                d = f.read()
                assert len(d) == args.length, "Differing lengths: Expected: " + str(args.length) + " but got: " + str(len(d))
                writeData(fs, args.offset, d)
            print("Read from: " + args.load + " and overwrote data at offset: " + str(args.offset) + " with length: " + str(len(d)))
        else:
            d = readData(fs, args.offset, args.length)
            if args.output:
                with open(args.output, "wb") as f:
                    f.write(d)
                print("Wrote: " + args.output)
