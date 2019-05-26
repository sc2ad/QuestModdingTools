import struct
import sys

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

def readFile(name):
    with open(name, "r+b") as f:
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
        f.write(str(o))

if __name__ == '__main__':
    if len(sys.argv == 2):
        print(readFile(sys.argv[1]))
    elif len(sys.argv == 3):
        s = readFile(sys.argv[1])
        serialize(s, sys.argv[2])
    else:
        print("Must provide a .dat raw export from UABE, and (optional) an output directory to save the .json")
