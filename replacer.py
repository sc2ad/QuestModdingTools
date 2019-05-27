import argparse
import os
import math
from splitter import *

from load_assets import *

songDir = "SongLevels"
levelCollectionsDir = "LevelCollections"
levelPacksDir = "LevelPacks"

def findData(assetJson, directory):
    songD = os.path.join(directory, songDir)
    levelCD = os.path.join(directory, levelCollectionsDir)
    levelPD = os.path.join(directory, levelPacksDir)
    try:
        os.mkdir(directory)
        os.mkdir(songD)
        os.mkdir(levelCD)
        os.mkdir(levelPD)
    except FileExistsError:
        pass
    for i in range(len(assetJson['Objects'])):
        obj = assetJson['Objects'][i]
        if obj['ClassID'] == 114:
            if obj['MonoScript']['PathID'] == 644:
                # Then this is a song level
                print("Found a song with name: " + obj['Name'] + " at index: " + str(i))
                serialize(obj, os.path.join(songD, obj['Name']) + ".json")
                print("Serialized JSON saved to: " + os.path.join(songD, obj['Name']))
            elif obj['MonoScript']['PathID'] == 762:
                # Then this is a beatmap level collection
                print("Found a beatmap level collection with name: " + obj['Name'] + " at index: " + str(i))
                serialize(obj, os.path.join(levelCD, obj['Name']) + ".json")
                print("Serialized JSON saved to: " + os.path.join(levelCD, obj['Name']))
            elif obj['MonoScript']['PathID'] == 1480:
                # Then this is a beatmap level pack
                print("Found a beatmap level pack with name: " + obj['Name'] + " at index: " + str(i))
                serialize(obj, os.path.join(levelPD, obj['Name']) + ".json")
                print("Serialized JSON saved to: " + os.path.join(levelPD, obj['Name']))
        

def overwriteJson(objects, metadata, header, index, data={}):
    bytecheck = False
    if 'ByteSize' in objects[index].keys():
        bytecheck = True
    if bytecheck:
        oldLen = objects[index]['ByteSize']
    nLen = oldLen
    for key in data.keys():
        if key == 'Offset':
            # Used to dynamically calculate offsets.
            continue
        if type(data[key]) == str:
            delta = len(data[key]) - len(objects[index][key])
            nLen += delta
            if delta != 0:
                print("Found delta with key: " + key + " with old: " + str(objects[index][key]) + " new: " + str(data[key]))
        elif type(data[key]) == dict:
            if 'Array' in data[key].keys():
                l = nLen
                for item in objects[index][key]['Array']:
                    nLen -= item['ByteSize']
                for item in data[key]['Array']:
                    nLen += item['ByteSize']
                if nLen != l:
                    print("Found delta with key: " + key + " in list with newLen: " + str(len(data[key]['Array'])) + " oldLen: " + str(len(objects[index][key]['Array'])))
        objects[index][key] = data[key]
    if bytecheck and nLen != oldLen:
        objects[index]['ByteSize'] = nLen
        for item in metadata['Objects']:
            if item['PathID'] == objects[index]['PathID']:
                # Matching item, update bytesize
                item['ByteSize'] = nLen
                break
        print("Updated JSON size: " + str(nLen) + " old: " + str(oldLen))
        # Shift all offsets after this json by: 4 * math.ceil(nLen - oldLen)
        delta = 4 * math.ceil((nLen - oldLen) / 4.0)
        print("Updated FileSize from: " + str(header['FileSize']) + " to: " + str(header['FileSize'] + delta))
        header['FileSize'] += delta
        for i in range(index + 1, len(objects)):
            # Not as simple as simple addition, need to align after every add
            print("Updating: " + objects[i]['Name'] + " Offset from: " + str(objects[i]['Offset']) + " to: " + str(objects[i]['Offset'] + delta))
            objects[i]['Offset'] += delta
            if not 'ReadOffset' in objects[i].keys():
                objects[i]['ReadOffset'] = 0
            objects[i]['ReadOffset'] += delta
            for item in metadata['Objects']:
                if item['PathID'] == objects[i]['PathID']:
                    # Matching item, increase offset
                    item['Offset'] += delta
    return objects

def addObject(assetJson, data, metadata):
    # Involves increasing the metadata length, adding a metadata and standard object, increasing the file length, and write the json
    index = assetJson['Metadata']['ObjectCount'] + 1

    metadataObjectSize = 20

    assetJson['Header']['MetadataSize'] += metadataObjectSize
    assetJson['Header']['FileSize'] += metadataObjectSize
    assetJson['Header']['DataOffset'] += metadataObjectSize

    metadata['PathID'] = index
    metadata['Offset'] = assetJson['Header']['FileSize'] - assetJson['Header']['DataOffset']
    data['PathID'] = index
    data['Offset'] = metadata['Offset']
    data['ByteSize'] = metadata['ByteSize']
    data['ClassID'] = 114 # Script class
    data['Fresh'] = True

    # metadata['ByteSize'] #TODO

    assetJson['Header']['FileSize'] += metadata['ByteSize']

    assetJson['Metadata']['ObjectCount'] += 1
    assetJson['Metadata']['Objects'].append(metadata)

    for item in assetJson['Objects']:
        if 'Fresh' in item.keys():
            continue
        if not 'ReadOffset' in item.keys():
            item['ReadOffset'] = 0
        item['ReadOffset'] += metadataObjectSize

    assetJson['Objects'].append(data)


def getAsset(path):
    if path.endswith(".json"):
        return deserialize(path)
    elif path.endswith(".assets"):
        with open(path, 'rb') as fs:
            return readAsset(fs)
    elif ".split" in path:
        f = path.split(".split")[0]
        combine(f)
        with open(f, 'rb') as fs:
            return readAsset(fs)

def saveAsset(asset, path, asset_path):
    if path.endswith(".json"):
        serialize(asset, path)
        print("Serialized modified asset to: " + path)
    elif path.endswith(".assets"):
        with open(path, 'wb') as fs:
            with open(asset_path, 'rb') as fr:
                writeAsset(fs, fr, asset)
        print("Wrote modified asset to: " + path)
    elif ".split" in path:
        f = path.split(".split")[0]
        if not f.endswith(".assets"):
            f += ".assets"
        with open(f, 'wb') as fs:
            with open(asset_path, 'rb') as fr:
                writeAsset(fs, fr, asset)
        split(f)
        print("Split asset!")

def getOffsetIncreasingObjectsList(assetJson):
    return sorted(assetJson['Objects'], key=lambda ob: ob['Offset'])
    
def setList(assetJson, i, obj, d, dire):
    print("Deserialized JSON read from: " + os.path.join(os.path.join(d, dire), obj['Name']))
    return overwriteJson(getOffsetIncreasingObjectsList(assetJson), assetJson['Metadata'], assetJson['Header'], i, deserialize(os.path.join(os.path.join(d, dire), obj['Name']) + ".json"))
def overwriteAllSongsFromDirectory(assetJson, directory):
    for i in range(len(assetJson['Objects'])):
        obj = assetJson['Objects'][i]
        if obj['ClassID'] == 114:
            if obj['MonoScript']['PathID'] == 644:
                # Then this is a song level
                print("Found a song with name: " + obj['Name'] + " at index: " + str(i))
                assetJson['Objects'] = setList(assetJson, i, obj, directory, songDir)
            elif obj['MonoScript']['PathID'] == 762:
                # Then this is a beatmap level collection
                print("Found a beatmap level collection with name: " + obj['Name'] + " at index: " + str(i))
                assetJson['Objects'] = setList(assetJson, i, obj, directory, levelCollectionsDir)
            elif obj['MonoScript']['PathID'] == 1480:
                # Then this is a beatmap level pack
                print("Found a beatmap level pack with name: " + obj['Name'] + " at index: " + str(i))
                assetJson['Objects'] = setList(assetJson, i, obj, directory, levelPacksDir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The main file for making changes to .assets. Allows for differing length read/writes.")
    parser.add_argument("asset_path", type=str, help="The path to the .assets file or append .split to read from splits. This also accepts .json files, but will not save as .assets or as .splits if chosen.")
    parser.add_argument("--json-out", type=str, help="The directory for the .json files of all the data.")
    parser.add_argument("--json-in", type=str, help="The directory to load the .json files of all the data to overwrite.")
    parser.add_argument("--output", type=str, help="The .json or .assets or .split file to output the modified .assets data. If .split is chosen, will first convert to .assets and then split.")
    parser.add_argument("--add-object", type=str, help="The path to a .json file to ADD as an object to the .assets data. This file must be structured very specifically.")

    args = parser.parse_args()

    asset = getAsset(args.asset_path)

    if args.add_object:
        d = deserialize(args.add_object)
        addObject(asset, d['Data'], d['Metadata'])

    if args.json_out:
        findData(asset, args.json_out)
    elif args.json_in:
        overwriteAllSongsFromDirectory(asset, args.json_in)
    
    if args.output:
        if not args.output.endswith('.json') and args.asset_path.endswith('.json'):
            print("Must provide .assets or .split file as 'asset_path' in order to save without serialization!")
        else:
            if '.split' in args.asset_path:
                args.asset_path = args.asset_path.split('.split')[0]
                assert args.asset_path.endswith('.assets'), ".split file must have .assets immediately before .split!"
            saveAsset(asset, args.output, args.asset_path)
