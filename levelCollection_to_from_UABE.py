import struct
import json
import argparse

from helper import *

### This file was auto-generated using uabe_autoparser.py
### Author: Sc2ad
def readBeatmapLevels(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for _ in range(o['size']):
        dat = {'data': readPtr(fs)}
        dat['ByteSize'] = 12
        o['Array'].append(dat)
    return o
def writeBeatmapLevels(fs, o):
    writeUInt32(fs, o['size'])
    for item in o['Array']:
        writePtr(fs, item['data'])
def readMonoBehaviour(fs, obj={}):
    o = {}
    o['GameObject'] = obj["GameObject"] if "GameObject" in obj.keys() else readPtr(fs)
    o['Enabled'] = obj["Enabled"] if "Enabled" in obj.keys() else readUInt32(fs)
    o['MonoScript'] = obj["MonoScript"] if "MonoScript" in obj.keys() else readPtr(fs)
    o['Name'] = obj["Name"] if "Name" in obj.keys() else readAlignedString(fs)
    o['_beatmapLevels'] = readBeatmapLevels(fs)
    return o
def writeMonoBehaviour(fs, o):
    writePtr(fs, o['GameObject'])
    writeUInt32(fs, o['Enabled'])
    writePtr(fs, o['MonoScript'])
    writeAlignedString(fs, o['Name'])
    writeBeatmapLevels(fs, o['_beatmapLevels'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Provides a converter for BeatmapLevelData from .dat files (exported from UABE)")
    parser.add_argument("file", type=str, help="The .dat file to load.")
    parser.add_argument('--output', type=str, help="The output directory for the serialized json.")
    parser.add_argument('--load', type=str, help="Will use the provided file in order to load the updates to the .dat file.")

    args = parser.parse_args()

    if args.load:
        dat = deserialize(args.load)
        print("Deserialized: " + str(dat))
        # Write the changes to the file.
        with open(args.file, "wb") as f:
            writeMonoBehaviour(f, dat)

    else:
        with open(args.file, "rb") as f:
            dat = readMonoBehaviour(f)

            print(dat)
            if args.output:
                serialize(dat, args.output)
                print("Serialized!")
