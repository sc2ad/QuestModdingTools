import struct
import argparse

from helper import *

def readBeatmaps(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for _ in range(o['size']):
        data = {}
        data['_beatmapCharacteristic'] = readPtr(fs)
        data['_difficultyBeatmaps'] = readDifficulties(fs)
        data['ByteSize'] = 12 + data['_difficultyBeatmaps']['size'] * data['_difficultyBeatmaps']['Array'][0]['ByteSize']
        o['Array'].append(data)
    return o

def writeBeatmaps(fs, o):
    writeUInt32(fs, o['size'])
    for item in o['Array']:
        writePtr(fs, item['_beatmapCharacteristic'])
        writeDifficulties(fs, item['_difficultyBeatmaps'])

def readDifficulties(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for _ in range(o['size']):
        data = {}
        data['_difficulty'] = readInt32(fs)
        data['_difficultyRank'] = readInt32(fs)
        data['_noteJumpMovementSpeed'] = readFloat(fs)
        data['_noteJumpStartBeatOffset'] = readInt32(fs)
        data['_beatmapData'] = readPtr(fs)
        data['ByteSize'] = 36
        o['Array'].append(data)
    return o

def writeDifficulties(fs, o):
    writeUInt32(fs, o['size'])
    for item in o['Array']:
        writeInt32(fs, item['_difficulty'])
        writeInt32(fs, item['_difficultyRank'])
        writeFloat(fs, item['_noteJumpMovementSpeed'])
        writeInt32(fs, item['_noteJumpStartBeatOffset'])
        writePtr(fs, item['_beatmapData'])

def readBeatmapLevel(f, o={}):
    obj = {}
    obj["GameObject"] = o["GameObject"] if "GameObject" in o.keys() else readPtr(f)
    obj["Enabled"] = o["Enabled"] if "Enabled" in o.keys() else readUInt32(f)
    obj["MonoScript"] = o["MonoScript"] if "MonoScript" in o.keys() else readPtr(f)
    obj["Name"] = o["Name"] if "Name" in o.keys() else readAlignedString(f)
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

def writeBeatmapLevel(f, obj):
    writePtr(f, obj["GameObject"])
    writeUInt32(f, obj["Enabled"])
    writePtr(f, obj["MonoScript"])
    writeAlignedString(f, obj["Name"])
    writeAlignedString(f, obj["_levelID"])
    writeAlignedString(f, obj["_songName"])
    writeAlignedString(f, obj["_songSubName"])
    writeAlignedString(f, obj["_songAuthorName"])
    writeAlignedString(f, obj["_levelAuthorName"])
    writePtr(f, obj["_audioClip"])
    writeFloat(f, obj["_beatsPerMinute"])
    writeFloat(f, obj["_songTimeOffset"])
    writeFloat(f, obj["_shuffle"])
    writeFloat(f, obj["_shufflePeriod"])
    writeFloat(f, obj["_preivewStartTime"])
    writeFloat(f, obj["_previewDuration"])
    writePtr(f, obj["_coverImageTexture2D"])
    writePtr(f, obj["_environmentSceneInfo"])
    writeBeatmaps(f, obj["_difficultyBeatmapSets"])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Provides a converter for BeatmapLevelData from .dat files (exported from UABE)")
    parser.add_argument("file", type=str, help="The .dat file to load.")
    parser.add_argument('--output', type=str, help="The output directory for the serialized json.")
    parser.add_argument('--load', type=str, help="Will use the provided file in order to load the updates to the .dat file.")

    args = parser.parse_args()

    if args.load:
        level = deserialize(args.load)
        print("Deserialized: " + str(level))
        # Write the changes to the file.
        with open(args.file, "wb") as f:
            # Write level
            writeBeatmapLevel(f, level)
            print("Wrote beatmap level to: " + args.file)
    else:
        with open(args.file, "rb") as f:
            level = readBeatmapLevel(f)
            print(level)
            if args.output:
                serialize(level, args.output)
                print("Serialized!")
