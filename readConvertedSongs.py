import beatmapDifficultyData_to_from_UABE as difficulty
import beatmapLevelData_to_from_UABE as levelData
import audioClip_to_from_UABE as audioClip
import texture2D_to_from_UABE as texture2d
import argparse
from helper import *
import resource_parser
import replacer
import os

# pip install sounddevice
import soundfile
from PIL import Image

LATEST_PID = 261

# diff = '../NUCLEAR-STAR/ExpertPlus.dat' # The output from songe_converter.exe
# diff = "../NUCLEAR-STAR/ExpertPlusBinary.dat" # Converted to binary version of ExpertPlus
# level = '../NUCLEAR-STAR/info.dat' # The output from songe_converter.exe

# songDir = '../NUCLEAR-STAR/' # The directory for the song.

# path_to_songe = 'songe-converter.exe'
commands = ['-k', '-g **/info.json']
resourcesPath = "assets/bin/Data"
sharedAssets = "sharedassets17.assets.split"

# path_to_beatmapCreator = 'BeatmapAssetMaker.exe'

# diffD = 'NuclearStarDifficulties'

# asset_path = "../UABE Dumps/sharedassets17.assets.split"
# json_out_dir = "ParsedData"
# output = "../UABE Dumps/sharedassets17-nuclearStar.assets.split"

# audioClipObjPath = 'NuclearStarAudioClip.json'
# o = 'NuclearStarExpertPlus.json'
# levelJson = 'NuclearStar.json'
# levelDat = 'NuclearStarLevelDat.dat'

def findDifficulties(songDir):
    fs = os.listdir(songDir)
    a = []
    for item in fs:
        if item.endswith('.dat') and not 'info' in item and not 'lyrics' in item:
            a.append(os.path.join(songDir, item))
    return a

def findImage(songDir):
    fs = os.listdir(songDir)
    for item in fs:
        if item.endswith('jpg'):
            return os.path.join(songDir, item)

def findInfo(songDir):
    fs = os.listdir(songDir)
    for item in fs:
        if item.endswith('info.dat'):
            return os.path.join(songDir, item)

def findOgg(songDir):
    fs = os.listdir(songDir)
    for item in fs:
        if item.endswith('.ogg'):
            return os.path.join(songDir, item)

def convertSong(exePath, path, commands):
    os.system(exePath + " " + ' '.join(commands) + " " + path)

def createBeatmapData(exePath, name, input_dat, output_asset):
    os.system(exePath + " " + name + " " + input_dat + " " + output_asset)

def createBeatmapDataObject(json_out, js, size):
    meta = {
        "TypeID": 14,
        "ByteSize": size
    }
    data = {
        "Metadata": meta,
        "Data": js
    }
    serialize(data, json_out)

def makeSongDifficulty(song_dat, out_dir, path_to_beatmapCreator):
    # n = song_dat.replace("/", "-")[3:][:-4]
    n = os.path.join(os.path.split(os.path.split(song_dat)[0])[1], os.path.split(song_dat)[1])[:-4]
    print(n)
    outF = os.path.join(out_dir, n + ".dat")
    if not os.path.exists(os.path.join(out_dir, os.path.split(n)[0])):
        os.mkdir(os.path.join(out_dir, os.path.split(n)[0]))

    createBeatmapData(path_to_beatmapCreator, n, song_dat, outF)

    with open(outF, 'rb') as fs:
        js = difficulty.readMonoBehaviour(fs)
        js['Name'] = n

    with open(outF, 'wb') as fs:
        difficulty.writeMonoBehaviour(fs, js)

    with open(outF, 'rb') as fs:
        size = len(fs.read())
        createBeatmapDataObject(os.path.join(out_dir, n + ".json"), js, size)
    return os.path.join(out_dir, n + ".json")

# Lengths should match.

def resetResource(res):
    bkp = '../UABE Dumps/bkp/' + res
    with open(res, 'wb') as fs:
        with open(bkp, 'rb') as f:
            print("Resetting res: " + res + " to: " + bkp)
            fs.write(f.read())

def makeTexture2D(name, image_path, json_path):
    OVERWRITE_BYTES = False
    meta = {
        "TypeID": 2,
        "ClassID": 28,
    }
    jpg = Image.open(image_path)
    print(jpg.bits, jpg.size, jpg.format)
    # Let us assume that these images are RGB24!
    data = {
        "Name": name + "Texture2D",
        "ForcedFallbackFormat": 4,
        "DownscaleFallback": False,
        "Width": jpg.size[0],
        "Height": jpg.size[1],
        "CompleteImageSize": jpg.size[0] * jpg.size[1],
        "TextureFormat": 3,
        "MipCount": 9,
        "IsReadable": False,
        "StreamingMipmaps": False,
        "StreamingMipmapsPriority": 0,
        "ImageCount": 1,
        "TextureDimension": 2,
        "TextureSettings": {
            "FilterMode": 2,
            "Aniso": 1,
            "MipBias": -1.0,
            "WrapU": 1,
            "WrapV": 1,
            "WrapW": 0
        },
        "LightmapFormat": 6,
        "ColorSpace": 1,
        "image": {
            "size": 0,
            "Array": []
        },
        "StreamData": {
            "Offset": 0,
            "Size": 0,
            "Path": ""
        }
    }
    if OVERWRITE_BYTES:
        imBytes = jpg.tobytes()
        with open(os.path.join("temp", "temp.raw"), 'wb') as fs:
            writeUInt32(fs, jpg.size[0] * jpg.size[1])
            fs.write(imBytes)
        with open(os.path.join("temp", "temp.raw"), 'rb') as fs:
            data['image'] = texture2d.readTypelessData(fs)
    else:
        # MUST MAKE SURE IMAGE IS IN THE APK RESOURCES FOLDER!
        data['StreamData']['Path'] = os.path.split(image_path)[1]
        with open(image_path, 'rb') as fs:
            data['StreamData']['Size'] = len(fs.read())
    with open(os.path.join("temp", "temp.dat"), 'wb') as fs:
        texture2d.writeTexture2D(fs, data)
    with open(os.path.join("temp", "temp.dat"), 'rb') as fs:
        meta['ByteSize'] = len(fs.read())
    
    serialize({"Metadata": meta, "Data": data}, os.path.join(json_path, name + "Texture2D.json"))
    return os.path.join(json_path, name + "Texture2D.json")

def makeAudioClip(name, oggF, json_path):
    # Read OGG:
    with open(oggF, 'rb') as f:
        ogg = f.read()

    delta = len(ogg)

    data, sampleRate = soundfile.read(oggF)

    # resetResource(res)
    # with open(res, 'rb') as fs:
    #     fSize = len(fs.read())
    # with open(res, 'wb') as fs:
    #     # The following line needs to ONLY run when the .resource file has not already had a song added to it.
    #     fs.seek(fSize)
    #     resource_parser.writeData(fs, ogg)

    # COPY .OGG FILE TO APK RESOURCES FOLDER, IT WILL BE REFERENCED!

    resource = {
        'Source': os.path.split(oggF)[1],
        'Offset': 0,
        'Size': delta
    }
    meta = {
        'TypeID': 5,
        "ClassID": 83
    }
    d = {
        "Name": name + "AudioClip",
        "LoadType": 1,
        "Channels": 2,
        "Frequency": sampleRate,
        "BitsPerSample": 16,
        "Length": len(data) / float(sampleRate),
        "IsTrackerFormat": False,
        "Ambisonic": False,
        "SubsoundIndex": 0,
        "PreloadAudioData": True,
        "LoadInBackground": True,
        "Legacy3D": False,
        "Resource": resource,
        "CompressionFormat": 1
    }

    with open(os.path.join("temp", name + ".dat"), 'wb') as fs:
        audioClip.writeAudioClip(fs, d)
    with open(os.path.join("temp", name + ".dat"), 'rb') as fs:
        size = len(fs.read())
        meta['ByteSize'] = size

    serialize({"Metadata": meta, "Data": d}, os.path.join(json_path, name + "AudioClip.json"))
    return os.path.join(json_path, name + "AudioClip.json")

def convertDifficulty(difficulty):
    if difficulty == 'Easy':
        return 0
    elif difficulty == 'Normal':
        return 1
    elif difficulty == 'Hard':
        return 2
    elif difficulty == 'Expert':
        return 3
    return 4

def makeLevel(n, level_dat, levelJson, level_out_dat, objects):
    out = deserialize(level_dat)

    arr = [
        {
            "_difficulty": convertDifficulty(out["_difficultyBeatmapSets"][i]['_difficultyBeatmaps'][0]['_difficulty']),
            "_difficultyRank": out["_difficultyBeatmapSets"][i]['_difficultyBeatmaps'][0]['_difficultyRank'],
            "_noteJumpMovementSpeed": out["_difficultyBeatmapSets"][i]['_difficultyBeatmaps'][0]['_noteJumpMovementSpeed'],
            "_noteJumpStartBeatOffset": out["_difficultyBeatmapSets"][i]['_difficultyBeatmaps'][0]['_noteJumpStartBeatOffset'],
            "_beatmapData": {
                "FileID": 0,
                "PathID": objects['Difficulties'][i]['pid']
            },
            "ByteSize": 28
        # } for i in range(len(out["_difficultyBeatmapSets"]))
        } for i in range(1) # Failsafe for offset bug due to extra creation of these difficulties. Just choose the first one for now.
    ]

    a = {
        "Data": {
            "GameObject": {
                "FileID": 0,
                "PathID": 0
            },
            "Enabled": 1,
            "MonoScript": {
                "FileID": 1,
                "PathID": 644
            },
            "Name": n,
            "_levelID": n,
            "_songName": out["_songName"],
            "_songSubName": out['_songSubName'],
            "_songAuthorName": out['_songAuthorName'],
            "_levelAuthorName": out['_levelAuthorName'],
            "_audioClip": {
                "FileID": 0,
                "PathID": objects['AudioClip']['pid']
            },
            "_beatsPerMinute": out['_beatsPerMinute'],
            "_songTimeOffset": out['_songTimeOffset'],
            "_shuffle": out['_shuffle'],
            "_shufflePeriod": out['_shufflePeriod'],
            "_previewStartTime": out['_previewStartTime'],
            "_previewDuration": out['_previewDuration'],
            "_coverImageTexture2D": {
                "FileID": 0,
                "PathID": objects['Texture2D']['pid']
            },
            "_environmentSceneInfo": {
                "FileID": 0,
                "PathID": 252
            },
            # ONLY TWO HANDED SUPPORT
            "_difficultyBeatmapSets": {
                "size": 1,
                "Array": [
                    {
                        "_beatmapCharacteristic": {
                            "FileID": 22,
                            "PathID": 1
                        },
                        "_difficultyBeatmaps": {
                            "size": len(arr),
                            "Array": arr
                        },
                        "ByteSize": sum([item['ByteSize'] for item in arr]) + 16
                    }
                ]
            }
        }
    }

    a['Metadata'] = {
        "TypeID": 15
    }

    with open(level_out_dat, 'wb') as fs:
        levelData.writeBeatmapLevel(fs, a['Data'])

    with open(level_out_dat, 'rb') as fs:
        size = len(fs.read())
        fs.seek(0)
        serialize(levelData.readBeatmapLevel(fs), levelJson)

    print("Calculated ByteSize for Level: " + str(size))
    a['Metadata']['ByteSize'] = size

    serialize(a, levelJson)

def createObjects(asset_path, allObjects, json_out_dir, output):
    asset = replacer.getAsset(asset_path)
    for data in allObjects:
        print("Created Objects: " + str(data))
        # print("With PIDs: " + str(pidAudioClip) + ", " + str(pidDifficultyObjects[0])+ ", " + str("?"))

        # print(data['Objects'])

        ind = asset['Metadata']['ObjectCount']

        for item in data['Objects'].keys():
            if type(data['Objects'][item]) == list:
                for v in data['Objects'][item]:
                    d = deserialize(v['path'])
                    replacer.addObject(asset, d['Data'], d['Metadata'])
            else:
                d = deserialize(data['Objects'][item]['path'])
                replacer.addObject(asset, d['Data'], d['Metadata'])

        replacer.findData(asset, json_out_dir)
        # replacer.findData(asset, json_out_dir, 0)

        # Edit ExtrasLevelCollection to add song
        j = deserialize(os.path.join(json_out_dir, os.path.join("LevelCollections", "ExtrasLevelCollection.json")))
        lev = deserialize(os.path.join(json_out_dir, os.path.join("SongLevels", data['Name'] + ".json")))

        j['_beatmapLevels']['size'] += 1

        levelPtr = {
            "data": {
                "FileID": 0,
                "PathID": lev['PathID']
            },
            "ByteSize": 12
        }
        j['_beatmapLevels']['Array'].append(levelPtr)
        j['ByteSize'] += levelPtr['ByteSize']

        serialize(j, os.path.join(json_out_dir, os.path.join("LevelCollections", "ExtrasLevelCollection.json")))

        replacer.overwriteAllSongsFromDirectory(asset, json_out_dir)

    # input("HOLD!")

    if '.split' in asset_path:
        asset_path = asset_path.split('.split')[0]
        assert asset_path.endswith('.assets'), ".split file must have .assets immediately before .split!"
    replacer.saveAsset(asset, output, asset_path)

    asset = replacer.getAsset(output)
    replacer.findData(asset, json_out_dir)

def addObj(name, data, path):
    global LATEST_PID
    if name in data['Objects'].keys():
        data['Objects'][name].append({'path': path, 'pid': LATEST_PID})
        LATEST_PID += 1
        return
    if type(path) == list:
        data['Objects'][name] = path
        return
    data['Objects'][name] = {'path': path, 'pid': LATEST_PID}
    LATEST_PID += 1
    
def createObjectsForSong(songDir, path_to_songe, path_to_beatmapCreator, json_path):
    name = deserialize(os.path.join(songDir, "info.json"))['songName']
    data = {"Name": name, "Objects" : {}}
    convertSong(path_to_songe, songDir, commands)
    diffs = findDifficulties(songDir)
    level = findInfo(songDir)

    addObj('Texture2D', data, makeTexture2D(name, findImage(songDir), json_path))
    addObj('AudioClip', data, makeAudioClip(name, findOgg(songDir), json_path))
    addObj('Difficulties', data, [])
    if not os.path.exists(os.path.join("temp", "difficulties")):
        os.mkdir(os.path.join("temp", "difficulties"))
    for diff in diffs:
        addObj('Difficulties', data, makeSongDifficulty(diff, os.path.join("temp", "difficulties"), path_to_beatmapCreator))
    makeLevel(name, level, os.path.join(json_path, name + "Level.json"), os.path.join("temp", name + "Level.json"), data['Objects'])
    addObj('Level', data, os.path.join(os.path.join(json_path, name + "Level.json")))
    return data

def createBackups(apkPath, backup):
    if not '.split' in apkPath and not apkPath.endswith('.assets'):
        dataDir = os.path.join(apkPath, resourcesPath)
    else:
        dataDir = os.path.split(apkPath)[0]
    for f in os.listdir(dataDir):
        if os.path.isdir(os.path.join(dataDir, f)):
            continue
        with open(os.path.join(dataDir, f), 'rb') as fs:
            with open(os.path.join(backup, f), 'wb') as fw:
                fw.write(fs.read())
    


if __name__ == "__main__":
    # GOAL: PROVIDE YOUR UNZIPPED APK AS A PATH, AND PROVIDE A LIST OF CUSTOM SONGS AND THIS WILL DO THE REST.
    # ABLE TO PARSE AND FIND ASSETS OF INTEREST
    # CREATE FOLDERS IN THE APK DIRECTORY FOR INSERTING
    # SPLITS AND UNSPLITS .ASSETS FILE (REMOVES UNSPLIT WHEN COMPLETE)
    # CREATES NEW DIRECTORIES FOR SONGS (WHICH CONTAIN THEIR .OGG AND .JPG FILES)
    # ADDS THESE SONGS TO THE EXTRA SONG PACK
    # WRITES USELESS FILES TO A TEMP DIRECTORY, WHICH IS THEN REMOVED.
    parser = argparse.ArgumentParser(description="A python script that handles the installation of custom songs onto your device.")
    parser.add_argument("path_to_apk", type=str, help="The path to your unzipped .apk root directory. Alternatively, you may provide a path to your .assets directly.")
    parser.add_argument("path_to_songs", type=str, help="The path to your songs.")
    parser.add_argument("path_to_songe_converter", type=str, help="The path to the songe-converter.exe.")
    parser.add_argument("path_to_beatmapassetmaker", type=str, help="The path to the BeatmapAssetMaker.exe.")
    parser.add_argument("--json-output", type=str, help="The path to save json output. Default = 'JsonOutput/'")
    parser.add_argument("--backup", type=str, help="The path to save your backups. Default: 'bkps/'")

    args = parser.parse_args()
    if not args.json_output:
        args.json_output = "JsonOutput"
    if not args.backup:
        args.backup = "bkps"

    if not os.path.exists(args.backup):
        os.mkdir(args.backup)
    
    createBackups(args.path_to_apk, args.backup)

    if not os.path.exists('temp'):
        os.mkdir('temp')

    allObjects = []

    dirpath = args.path_to_songs

    for d in os.listdir(args.path_to_songs):
        allObjects.append(createObjectsForSong(os.path.join(dirpath, d), args.path_to_songe_converter, args.path_to_beatmapassetmaker, args.json_output))

    # NEED TO RESTRUCTURE!
    if not os.path.exists(args.json_output):
        os.mkdir(args.json_output)

    tempAssets = os.path.join("temp", "Assets")
    if not os.path.exists(tempAssets):
        os.mkdir(tempAssets)
    if not args.path_to_apk.endswith(".assets") and not '.split' in args.path_to_apk:
        dataFolder = os.path.join(args.path_to_apk, resourcesPath)
        assetSpot = sharedAssets
    else:
        dataFolder = os.path.split(args.path_to_apk)[0]
        if '.split' in args.path_to_apk:
            assetSpot = args.path_to_apk.split('.split')[0]
        else:
            assetSpot = args.path_to_apk
    createObjects(os.path.join(dataFolder, assetSpot), allObjects, args.json_output, os.path.join(tempAssets, sharedAssets))
    print("Copying Assets!")
    for f in os.listdir(tempAssets):
        if f.endswith(".assets"):
            continue
        with open(os.path.join(tempAssets, f), 'rb') as fs:
            with open(os.path.join(dataFolder, f), 'wb') as fw:
                fw.write(fs.read())
    print("Copying songs/pictures!")
    for d in os.listdir(args.path_to_songs):
        image = findImage(os.path.join(args.path_to_songs, d))
        ogg = findOgg(os.path.join(args.path_to_songs, d))
        with open(image, 'rb') as fs:
            with open(os.path.join(dataFolder, os.path.split(image)[1]), 'wb') as fw:
                fw.write(fs.read())
        with open(ogg, 'rb') as fs:
            with open(os.path.join(dataFolder, os.path.split(ogg)[1]), 'wb') as fw:
                fw.write(fs.read())
    print("Complete!")
