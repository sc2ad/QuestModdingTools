# Loads a .assets file (or multiple .assets.split* files) and parses them at given offsets.

import argparse
import struct
import json

from helper import *
import beatmapDifficultyData_to_from_UABE as difficultyData
import beatmapLevelData_to_from_UABE as levelData
import audioClip_to_from_UABE as audioClip

# This audio clip has fileID = 0, pathID = 28
memOffsetForAudioClip = 0x00684a38
# This audio clip has fileID = 0, pathID = 29
memOffsetForAudioClip2 = 0x00684a98

# d = "../UABE Dumps/sharedassets17.assets"
# outp = "../UABE Dumps/sharedassets17.assets.json"

def readHeader(fs):
    o = {}
    o['MetadataSize'] = readUInt32(fs, '>')
    o['FileSize'] = readUInt32(fs, '>')
    o['Generation'] = readUInt32(fs, '>')
    o['DataOffset'] = readUInt32(fs, '>')
    o['IsBigEndian'] = readUInt32(fs, '>')
    return o

def writeHeader(fs, o):
    writeUInt32(fs, o['MetadataSize'], '>')
    writeUInt32(fs, o['FileSize'], '>')
    writeUInt32(fs, o['Generation'], '>')
    writeUInt32(fs, o['DataOffset'], '>')
    writeUInt32(fs, o['IsBigEndian'], '>')

def readType(fs):
    o = {}
    o["ClassID"] = readUInt32(fs)
    o["IsStripped"] = readUInt8(fs)
    o["ScriptTypeIndex"] = readInt16(fs)
    if o['ClassID'] == 114:
        o['ScriptID'] = readHex16(fs)
    o['TypeHash'] = readHex16(fs)
    return o

def writeType(fs, o):
    writeUInt32(fs, o["ClassID"])
    writeUInt8(fs, o["IsStripped"])
    writeInt16(fs, o["ScriptTypeIndex"])
    if o['ClassID'] == 114:
        writeHex16(fs, o['ScriptID'])
    writeHex16(fs, o['TypeHash'])

def readTypes(fs, count):
    o = {}
    # readAlign(fs, fs.tell())
    for i in range(count):
        o[i] = readType(fs)
    return o

def readObjects(fs, count, types):
    a = []
    for _ in range(count):
        o = {}
        readAlign(fs, fs.tell())
        o['PathID'] = readUInt64(fs)
        o['Offset'] = readUInt32(fs)
        o['ByteSize'] = readUInt32(fs)
        o['TypeID'] = readUInt32(fs)
        o['ClassID'] = types[o['TypeID']]['ClassID']
        a.append(o)
    return a

def readScripts(fs, count):
    a = []
    for _ in range(count):
        o = {}
        o['FileIndex'] = readUInt32(fs)
        readAlign(fs, fs.tell())
        o['LocalID'] = readUInt64(fs)
        a.append(o)
    return a

def readExternals(fs, count):
    a = []
    for _ in range(count):
        o = {}
        o['Temp'] = readCString(fs)
        o['GUID'] = hex(readUInt32(fs))
        o['Type'] = readUInt32(fs)
        o['PathName'] = readCString(fs)
        a.append(o)
    return a

def readMetadata(fs):
    o = {}
    o['UnityVersion'] = readCString(fs)
    o['TargetPlatform'] = readUInt32(fs)
    o['EnableTypeTree'] = readUInt8(fs)
    # readAlign(fs, fs.tell())
    o['TypeCount'] = readUInt32(fs)
    o['Types'] = readTypes(fs, o['TypeCount'])
    o['ObjectCount'] = readUInt32(fs)
    o['Objects'] = readObjects(fs, o['ObjectCount'], o['Types'])
    o['ScriptCount'] = readUInt32(fs)
    o['Scripts'] = readScripts(fs, o['ScriptCount'])
    o['ExternalsCount'] = readUInt32(fs)
    o['Externals'] = readExternals(fs, o['ExternalsCount'])
    return o

def readBehaviour(fs):
    o = {}
    o['GameObject'] = readPtr(fs)
    o['Enabled'] = readUInt32(fs)
    o['MonoScript'] = readPtr(fs)
    # o['ScriptExportID'] = readUInt32(fs)
    # o['Kind'] = readUInt64(fs)
    o['Name'] = readAlignedString(fs)

    if o['MonoScript']['PathID'] == 644:
        print("Attempting to read beatmap level...")
        o = levelData.readBeatmapLevel(fs, o)
    elif o['MonoScript']['PathID'] == 1552:
        print("Attempting to read Beatmap Data...")
        o = difficultyData.readMonoBehaviour(fs, o)
    return o

def readAsset(fs):
    o = {}
    o['Header'] = readHeader(fs)
    o['Metadata'] = readMetadata(fs)
    fs.seek(o['Header']['DataOffset'])
    o['DataLength'] = o['Header']['FileSize'] - o['Header']['DataOffset']
    o['Objects'] = []
    for obj in o['Metadata']['Objects']:
        fs.seek(o['Header']['DataOffset'] + obj['Offset'])
        if obj['ClassID'] == 114:
            o['Objects'].append(readBehaviour(fs))
            print("Interpretting data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as MonoBehaviour")
        elif obj['ClassID'] == 83:
            o['Objects'].append(audioClip.readAudioClip(fs))
            print("Interpretting data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as AudioClip")
    
    return o

def writeAsset(fs, o):
    writeHeader(o['Header'])
    writeMetadata(o['Metadata'])
    write0(fs, o['Header']['DataOffset'] - fs.tell())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for loading and writing .assets files into legible json.")
    parser.add_argument("path", type=str, help="The path to a packaged (full) .assets file.")
    parser.add_argument("output", type=str, help="The path to the resulting .json file")
    parser.add_argument("--load", help="Load the .json and overwrite the .assets at path. Default=false")

    args = parser.parse_args()

    if args.load:
        o = deserialize(args.output)
        print("Deserialized!")
        print("Writing...")
        writeAsset(fs, o)
        print("Wrote asset to: " + args.path)
    else:
        with open(args.path, 'rb') as fs:
            o = readAsset(fs)
            serialize(o, args.output)
            print("Serialized to: " + args.output)