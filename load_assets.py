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

def writeTypes(fs, o):
    for item in o.keys():
        writeType(fs, o[item])

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

def writeObjects(fs, a):
    for o in a:
        writeAlign(fs, fs.tell())
        writeUInt64(fs, o['PathID'])
        writeUInt32(fs, o['Offset'])
        writeUInt32(fs, o['ByteSize'])
        writeUInt32(fs, o['TypeID'])

def readScripts(fs, count):
    a = []
    for _ in range(count):
        o = {}
        o['FileIndex'] = readUInt32(fs)
        readAlign(fs, fs.tell())
        o['LocalID'] = readUInt64(fs)
        a.append(o)
    return a

def writeScripts(fs, a):
    for o in a:
        writeUInt32(fs, o['FileIndex'])
        writeAlign(fs, fs.tell())
        writeUInt64(fs, o['LocalID'])

def readExternals(fs, count):
    a = []
    for _ in range(count):
        o = {}
        o['Temp'] = readCString(fs, False)
        o['GUID'] = readHex16(fs)
        o['Type'] = readUInt32(fs)
        o['PathName'] = readCString(fs, False)
        read(fs, 1)
        a.append(o)
    return a

def writeExternals(fs, a):
    for o in a:
        writeCString(fs, o['Temp'], False)
        writeHex16(fs, o['GUID'])
        writeUInt32(fs, o['Type'])
        writeCString(fs, o['PathName'], False)

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

def writeMetadata(fs, o):
    writeCString(fs, o['UnityVersion'])
    writeUInt32(fs, o['TargetPlatform'])
    writeUInt8(fs, o['EnableTypeTree'])
    writeUInt32(fs, o['TypeCount'])
    writeTypes(fs, o['Types'])
    writeUInt32(fs, o['ObjectCount'])
    writeObjects(fs, o['Objects'])
    writeUInt32(fs, o['ScriptCount'])
    writeScripts(fs, o['Scripts'])
    writeUInt32(fs, o['ExternalsCount'])
    writeExternals(fs, o['Externals'])

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

def writeBehaviour(fs, o):
    if o['MonoScript']['PathID'] == 644:
        print("Attempting to write beatmap level...")
        levelData.writeBeatmapLevel(fs, o)
        return True
    elif o['MonoScript']['PathID'] == 1552:
        print("Attempting to write Beatmap Data...")
        difficultyData.writeMonoBehaviour(fs, o)
        return True
    else:
        # writePtr(fs, o['GameObject'])
        # writeUInt32(fs, o['Enabled'])
        # writePtr(fs, o['MonoScript'])
        # writeAlignedString(fs, o['Name'])
        return False

def readAsset(fs):
    o = {}
    o['Header'] = readHeader(fs)
    o['Metadata'] = readMetadata(fs)
    print("Current: " + str(fs.tell()) + " Metadata end: " + str(o['Header']['MetadataSize'] + 20))
    print("Going to data offset: " + str(o['Header']['DataOffset']))
    fs.seek(o['Header']['DataOffset'])
    o['DataLength'] = o['Header']['FileSize'] - o['Header']['DataOffset']
    o['Objects'] = []
    for obj in o['Metadata']['Objects']:
        fs.seek(o['Header']['DataOffset'] + obj['Offset'])
        dat = {}
        if obj['ClassID'] == 114:
            dat = readBehaviour(fs)
            print("Interpretting data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as MonoBehaviour")
        elif obj['ClassID'] == 83:
            dat = audioClip.readAudioClip(fs)
            print("Interpretting data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as AudioClip")
        dat['Offset'] = obj['Offset']
        dat['PathID'] = obj['PathID']
        dat['ClassID'] = obj['ClassID']
        dat['ByteSize'] = obj['ByteSize']
        o['Objects'].append(dat)
    return o

def writeMiddleData(fs, fr, offset, length, readOffset=0):
    fr.seek(offset - readOffset)
    fs.write(fr.read(length))

def copyData(fs, fr, offset, length, obj):
    if 'ReadOffset' in obj.keys():
        writeMiddleData(fs, fr, offset, length, obj['ReadOffset'])
    else:
        writeMiddleData(fs, fr, offset, length)

def writeAsset(fs, fr, o):
    writeHeader(fs, o['Header'])
    writeMetadata(fs, o['Metadata'])
    # write0(fs, o['Header']['DataOffset'] - fs.tell())
    writeMiddleData(fs, fr, fs.tell(), o['Header']['DataOffset'] - fs.tell())
    objects = sorted(o['Objects'], key=lambda ob: ob['Offset'])
    for i in range(len(objects)):
        obj = objects[i]
        # Need to somehow do proper seeking (write the other info too) but don't just fill it with 0s
        # We want to write the old data in order of increasing offset (hopefully this works?)
        if i == 0:
            print("Writing skip data: " + str(o['Header']['DataOffset']) + " with length: " + str(obj['Offset']))
            copyData(fs, fr, o['Header']['DataOffset'], obj['Offset'], obj)
        else:
            if objects[i]['Offset'] < objects[i-1]['Offset'] + objects[i-1]['ByteSize']:
                print(str(objects[i-1]))
            print("Writing skip data: " + str(o['Header']['DataOffset'] + objects[i-1]['Offset'] + objects[i-1]['ByteSize']) + " with length: " + str(obj['Offset'] - objects[i-1]['Offset'] - objects[i-1]['ByteSize']))
            copyData(fs, fr, o['Header']['DataOffset'] + objects[i-1]['Offset'] + objects[i-1]['ByteSize'], obj['Offset'] - objects[i-1]['Offset'] - objects[i-1]['ByteSize'], obj)

        if obj['ClassID'] == 114:
            print("Writing data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as MonoBehaviour with size: " + str(obj['ByteSize']))
            if not writeBehaviour(fs, obj):
                print("Writing data at: " + str(obj['ByteSize'] + obj['Offset'] + o['Header']['DataOffset']) + " as unknown MonoBehaviour with size: " + str(obj['ByteSize']))
                copyData(fs, fr, fs.tell(), obj['ByteSize'], obj)
            else:
                end = obj['ByteSize'] + obj['Offset'] + o['Header']['DataOffset']
                # print("Expected end: " + str(end) + " actual end: " + str(fs.tell()))
                if end - fs.tell() > 4:
                    print("Delta expected detected! delta: " + str(end - fs.tell()) + " obj info: " + str(obj))
                copyData(fs, fr, fs.tell(), obj['ByteSize'] + obj['Offset'] + o['Header']['DataOffset'] - fs.tell(), obj)
        elif obj['ClassID'] == 83:
            print("Writing data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as AudioClip with size: " + str(obj['ByteSize']))
            audioClip.writeAudioClip(fs, obj)
        else:
            print("Writing data at: " + str(o['Header']['DataOffset'] + obj['Offset']) + " as unknown raw copy with size: " + str(obj['ByteSize']))
            copyData(fs, fr, obj['Offset'] + o['Header']['DataOffset'], obj['ByteSize'], obj)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for loading and writing .assets files into legible json.")
    parser.add_argument("path", type=str, help="The path to a packaged (full) .assets file.")
    parser.add_argument("output", type=str, help="The path to the resulting .json file")
    parser.add_argument("--load", help="Load the .json and overwrite the .assets at this path.")

    args = parser.parse_args()

    if args.load:
        o = deserialize(args.output)
        print("Deserialized!")
        print("Writing...")
        with open(args.load, 'wb') as fs:
            with open(args.path, 'rb') as fr:
                writeAsset(fs, fr, o)
                print("Wrote asset to: " + args.load)
    else:
        with open(args.path, 'rb') as fs:
            print("Reading...")
            o = readAsset(fs)
            serialize(o, args.output)
            print("Serialized to: " + args.output)