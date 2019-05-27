import argparse
import os
import math
from splitter import *

from load_assets import *

def findSongLevels(assetJson, directory):
    for i in range(len(assetJson['Objects'])):
        obj = assetJson['Objects'][i]
        if obj['ClassID'] == 114:
            if obj['MonoScript']['PathID'] == 644:
                # Then this is a song level
                print("Found a song with name: " + obj['Name'] + " at index: " + str(i))
                serialize(obj, os.path.join(directory, obj['Name']) + ".json")
                print("Serialized JSON saved to: " + os.path.join(directory, obj['Name']))

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
        try:
            delta = len(data[key]) - len(objects[index][key])
            nLen += delta
            if delta != 0:
                print("Found delta with key: " + key + " with old: " + str(objects[index][key]) + " new: " + str(data[key]))
        except TypeError:
            # Not a container, static size
            pass
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
    
def overwriteAllSongsFromDirectory(assetJson, directory):
    for i in range(len(assetJson['Objects'])):
        obj = assetJson['Objects'][i]
        if obj['ClassID'] == 114:
            if obj['MonoScript']['PathID'] == 644:
                # Then this is a song level
                print("Found a song with name: " + obj['Name'] + " at index: " + str(i))
                assetJson['Objects'] = overwriteJson(getOffsetIncreasingObjectsList(assetJson), assetJson['Metadata'], assetJson['Header'], i, deserialize(os.path.join(directory, obj['Name']) + ".json"))
                print("Deserialized JSON read from: " + os.path.join(directory, obj['Name']))

asset_path = "../UABE Dumps/sharedassets17.assets"
json_path = "../UABE Dumps/sharedassets17.assets.json"
d = "RetrievedSongLevels/"
out2 = "../UABE Dumps/sharedassets17-modified.assets.json"
out = "../UABE Dumps/sharedassets17-modified.assets.split"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The main file for making changes to .assets. Allows for differing length read/writes.")
    parser.add_argument("asset_path", type=str, help="The path to the .assets or .split file. This also accepts .json files, but will not save .assets or .splits.")
    parser.add_argument("--level-out", type=str, help="The directory for the .json files of all the level data.")
    parser.add_argument("--level-in", type=str, help="The directory to load the .json files of all the level data to overwrite.")
    parser.add_argument("--output", type=str, help="The .json or .assets or .split file to output the modified .assets data. If .split is chosen, will first convert to .assets and then split.")
    
    args = parser.parse_args()

    asset = getAsset(args.asset_path)
    if args.level_out:
        findSongLevels(asset, args.level_out)
    elif args.level_in:
        overwriteAllSongsFromDirectory(asset, args.level_in)
    
    if args.output:
        if not args.output.endswith('.json') and args.asset_path.endswith('.json'):
            print("Must provide .assets or .split file as 'asset_path' in order to save without serialization!")
        else:
            if '.split' in args.asset_path:
                args.asset_path = args.asset_path.split('.split')[0]
                assert args.asset_path.endswith('.assets'), ".split file must have .assets immediately before .split!"
            saveAsset(asset, args.output, args.asset_path)
