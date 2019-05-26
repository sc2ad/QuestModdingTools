import struct
import json
import argparse

def read(fs, n):
    return fs.read(n)

def readAlignedString(fs):
    length = readUInt8(fs)
    i = 0
    s = ""
    if length == 0:
        # Throwaway to be aligned again.
        read(fs, 3)
        return ""
    while i < length:
        item = read(fs, 1)
        if item == b'\x00':
            continue
        s += item.decode()
        i += 1
    read(fs, (4 - i) % 4)
    return s

def readUInt8(fs):
    return struct.unpack("B", read(fs, 1))[0]

def readInt32(fs):
    return struct.unpack("i", read(fs, 4))[0]

def readUInt32(fs):
    return struct.unpack("I", read(fs, 4))[0]

def readFloat(fs):
    return struct.unpack("f", read(fs, 4))[0]

def readInt64(fs):
    return struct.unpack("q", read(fs, 8))[0]

def readPtr(fs):
    d = {}
    d['FileID'] = readInt32(fs)
    d['PathID'] = readInt64(fs)
    return d

def readBeatmaps(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for i in range(o['size']):
        data = {}
        data['_beatmapCharacteristic'] = readPtr(fs)
        data['_difficultyBeatmaps'] = readDifficulties(fs)
        o['Array'].append(data)
    return o

def readDifficulties(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for i in range(o['size']):
        data = {}
        data['_difficulty'] = readInt32(fs)
        data['_difficultyRank'] = readInt32(fs)
        data['_noteJumpMovementSpeed'] = readFloat(fs)
        data['_noteJumpStartBeatOffset'] = readInt32(fs)
        data['_beatmapData'] = readPtr(fs)
        o['Array'].append(data)
    return o

def readBeatmapLevel(fs):
    obj = {}
    obj["GameObject"] = readPtr(f)
    obj["Enabled"] = readUInt32(f)
    obj["MonoScript"] = readPtr(f)
    obj["Name"] = readAlignedString(f)
    obj["_levelID"] = readAlignedString(f)
    obj["_songName"] = readAlignedString(f)
    obj["_songSubName"] = readAlignedString(f)
    obj["_songAuthorName"] = readAlignedString(f)
    obj["_levelAuthorName"] = readAlignedString(f)
    obj["_audioClip"] = readPtr(f)
    obj["_beatsPerMinute"] = readFloat(f)
    obj["_songTimeOffset"] = readFloat(f)
    obj["_shuffle"] = readFloat(f)
    obj["_shufflePeriod"] = readFloat(f)
    obj["_preivewStartTime"] = readFloat(f)
    obj["_previewDuration"] = readFloat(f)
    obj["_coverImageTexture2D"] = readPtr(f)
    obj["_environmentSceneInfo"] = readPtr(f)
    obj["_difficultyBeatmapSets"] = readBeatmaps(f)
    return obj

def serialize(o, p):
    with open(p, "w") as f:
        json.dump(o, f, skipkeys=True)

def deserialize(p):
    with open(p, 'r') as f:
        return json.load(f)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Provides a converter for BeatmapLevelData from .dat files (exported from UABE)")
    parser.add_argument("file", type=str, help="The .dat file to load.")
    parser.add_argument('--output', type=str, help="The output directory for the serialized json.")
    parser.add_argument('--load', type=str, help="Will use the provided file in order to load the updates to the .dat file.")

    args = parser.parse_args()

    if args.load:
        level = deserialize(args.load)
        print("Deserialized: " + level)
        # Write the changes to the file.
        with open(args.file, "w+b") as f:
            # Write level
            pass
    else:
        with open(args.file, "r+b") as f:
            level = readBeatmapLevel(f)
            print(level)
            if args.output:
                serialize(level, args.output)
                print("Serialized!")
