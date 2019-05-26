import argparse
import os

SPLIT_SIZE = 1024 * 1024

def split(mainAssetName):
    with open(mainAssetName, 'rb') as fs:
        fs.seek(0)
        index = 0
        while len(fs.peek()) > 0:
            with open(mainAssetName + '.split' + str(index), 'wb') as f:
                f.write(fs.read(SPLIT_SIZE))
            print("Wrote: " + mainAssetName + '.split' + str(index))
            index += 1

def combine(mainAssetPath):
    d, name = os.path.split(mainAssetPath)

    if name.endswith(".split0"):
        name = name[:len(name) - 7]
    with open(os.path.join(d, name), 'wb') as fs:
        for (path, dirs, files) in os.walk(d):
            for f in files:
                if f.startswith(name) and f != name:
                    with open(os.path.join(d, f), 'rb') as fr:
                        fs.write(fr.read())
                    print("Read: " + os.path.join(d, f))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Handles splitting to and from .split* files.")
    parser.add_argument("path", type=str, help="The path to the .asset to read from or write to.")
    parser.add_argument("mode", type=int, help="The mode to use. Choose 0 for splitting, 1 for combining.", default=1)

    args = parser.parse_args()

    if args.mode == 1:
        combine(args.path)
    elif args.mode == 0:
        split(args.path)
    else:
        print("Invalid mode!")
