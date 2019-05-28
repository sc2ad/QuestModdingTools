import beatmapDifficultyData_to_from_UABE as difficulty
import beatmapLevelData_to_from_UABE as levelData
import argparse
from helper import *
import resource_parser
import replacer
import os

diff = '../NUCLEAR-STAR/ExpertPlus.dat'
level = '../NUCLEAR-STAR/info.dat'
diffD = 'NuclearStarExpertPlus.dat'
oggF = '../NUCLEAR-STAR/NUCLEAR.ogg'
res = 'sharedassets17.resource'

asset_path = "../UABE Dumps/sharedassets17.assets.split"
json_out_dir = "ParsedData"
output = "../UABE Dumps/sharedassets17-nuclearStar.assets.split"

pidDifficultyObjects = [262]
pidAudioClip = 261

audioClipObjPath = 'NuclearStarAudioClip.json'
o = 'NuclearStarExpertPlus.json'
levelJson = 'NuclearStarLevel.json'
levelDat = 'NuclearStarLevelDat.dat'

def createSongDifficultyObject(name, jDat, bts, out):
    
    s = """{ "GameObject": {
            "FileID": 0,
            "PathID": 0
        },
        "Enabled": 1,
        "MonoScript": {
            "FileID": 1,
            "PathID": 1552
        },
        "Name": \"""" + name + """\",
        "_jsonData": \"""" + jDat + """\",
        "_signatureBytes": {
            "size": 128,
            "Array": [
                {
                    "data": 8
                },
                {
                    "data": 198
                },
                {
                    "data": 115
                },
                {
                    "data": 75
                },
                {
                    "data": 215
                },
                {
                    "data": 206
                },
                {
                    "data": 89
                },
                {
                    "data": 70
                },
                {
                    "data": 233
                },
                {
                    "data": 182
                },
                {
                    "data": 197
                },
                {
                    "data": 133
                },
                {
                    "data": 142
                },
                {
                    "data": 237
                },
                {
                    "data": 112
                },
                {
                    "data": 138
                },
                {
                    "data": 132
                },
                {
                    "data": 107
                },
                {
                    "data": 199
                },
                {
                    "data": 52
                },
                {
                    "data": 164
                },
                {
                    "data": 97
                },
                {
                    "data": 185
                },
                {
                    "data": 215
                },
                {
                    "data": 145
                },
                {
                    "data": 44
                },
                {
                    "data": 217
                },
                {
                    "data": 240
                },
                {
                    "data": 64
                },
                {
                    "data": 163
                },
                {
                    "data": 250
                },
                {
                    "data": 196
                },
                {
                    "data": 172
                },
                {
                    "data": 40
                },
                {
                    "data": 79
                },
                {
                    "data": 111
                },
                {
                    "data": 236
                },
                {
                    "data": 15
                },
                {
                    "data": 17
                },
                {
                    "data": 79
                },
                {
                    "data": 27
                },
                {
                    "data": 220
                },
                {
                    "data": 165
                },
                {
                    "data": 93
                },
                {
                    "data": 241
                },
                {
                    "data": 237
                },
                {
                    "data": 236
                },
                {
                    "data": 245
                },
                {
                    "data": 56
                },
                {
                    "data": 164
                },
                {
                    "data": 206
                },
                {
                    "data": 40
                },
                {
                    "data": 89
                },
                {
                    "data": 142
                },
                {
                    "data": 191
                },
                {
                    "data": 202
                },
                {
                    "data": 49
                },
                {
                    "data": 32
                },
                {
                    "data": 214
                },
                {
                    "data": 175
                },
                {
                    "data": 43
                },
                {
                    "data": 62
                },
                {
                    "data": 103
                },
                {
                    "data": 132
                },
                {
                    "data": 139
                },
                {
                    "data": 203
                },
                {
                    "data": 105
                },
                {
                    "data": 0
                },
                {
                    "data": 84
                },
                {
                    "data": 128
                },
                {
                    "data": 20
                },
                {
                    "data": 184
                },
                {
                    "data": 59
                },
                {
                    "data": 158
                },
                {
                    "data": 146
                },
                {
                    "data": 106
                },
                {
                    "data": 159
                },
                {
                    "data": 75
                },
                {
                    "data": 56
                },
                {
                    "data": 157
                },
                {
                    "data": 207
                },
                {
                    "data": 244
                },
                {
                    "data": 188
                },
                {
                    "data": 49
                },
                {
                    "data": 156
                },
                {
                    "data": 18
                },
                {
                    "data": 190
                },
                {
                    "data": 120
                },
                {
                    "data": 208
                },
                {
                    "data": 66
                },
                {
                    "data": 244
                },
                {
                    "data": 196
                },
                {
                    "data": 3
                },
                {
                    "data": 45
                },
                {
                    "data": 95
                },
                {
                    "data": 171
                },
                {
                    "data": 14
                },
                {
                    "data": 134
                },
                {
                    "data": 243
                },
                {
                    "data": 26
                },
                {
                    "data": 54
                },
                {
                    "data": 55
                },
                {
                    "data": 25
                },
                {
                    "data": 225
                },
                {
                    "data": 130
                },
                {
                    "data": 76
                },
                {
                    "data": 45
                },
                {
                    "data": 234
                },
                {
                    "data": 20
                },
                {
                    "data": 251
                },
                {
                    "data": 255
                },
                {
                    "data": 250
                },
                {
                    "data": 210
                },
                {
                    "data": 119
                },
                {
                    "data": 227
                },
                {
                    "data": 251
                },
                {
                    "data": 107
                },
                {
                    "data": 155
                },
                {
                    "data": 36
                },
                {
                    "data": 145
                },
                {
                    "data": 121
                },
                {
                    "data": 163
                },
                {
                    "data": 28
                },
                {
                    "data": 74
                },
                {
                    "data": 39
                },
                {
                    "data": 20
                },
                {
                    "data": 253
                },
                {
                    "data": 123
                }
            ]
        },"""
    with open(out, 'w') as f:
        f.write("{\n")
        f.write("\t\"Metadata\": {\n")
        f.write("\t\t\"TypeID\": 14,\n")
        f.write("\t\t\"ByteSize\": " + str(bts) + "\n")
        f.write("\t},\n")
        f.write("\t\"Data\": ")
        f.write(s+"\n")
        f.write("\t\t\"_projectedData\": {\"size\": 0, \"Array\": []")
        f.write("}\n\t}\n}")

out = deserialize(diff)
n = "NuclearStarExpertPlus"
size = 28 + len(n) + 4 + len(str(out)) + 4 + 132 + 4 + 4
size += 4 - size % 4
print(size)
createSongDifficultyObject(n, str(out), size, o)

with open(diffD, 'wb') as fs:
    difficulty.writeMonoBehaviour(fs, deserialize(o)['Data'])

with open(diffD, 'rb') as fs:
    r = len(fs.read())
    fs.seek(0)
    ok = difficulty.readMonoBehaviour(fs)
    print(len(ok))
    print(len(deserialize(o)['Data']))
    assert r == size, "Redefine size to be: " + str(r)

# Lengths should match.

# Read OGG:
with open(oggF, 'rb') as f:
    ogg = f.read()

delta = len(ogg)


with open(res, 'r+b') as fs:
    size = len(fs.read()) - delta
#     resource_parser.writeData(fs, size, ogg)

n = "NuclearStar"

resource = {
    'Source': "sharedassets17.resource",
    'Offset': size,
    'Size': delta
}
meta = {
    'ByteSize': 96,
    'TypeID': 5,
    "ClassID": 83
}
d = {
    "Name": n,
    "LoadType": 1,
    "Channels": 2,
    "Frequency": 44100,
    "BitsPerSample": 16,
    "Length": 268.1,
    "IsTrackerFormat": False,
    "Ambisonic": False,
    "SubsoundIndex": 0,
    "PreloadAudioData": True,
    "LoadInBackground": True,
    "Legacy3D": False,
    "Resource": resource,
    "CompressionFormat": 1
}

serialize({"Metadata": meta, "Data": d}, audioClipObjPath)

out = deserialize(level)

arr = [
    {
        "_difficulty": 4,
        "_difficultyRank": item['_difficultyBeatmaps'][0]['_difficultyRank'],
        "_noteJumpMovementSpeed": item['_difficultyBeatmaps'][0]['_noteJumpMovementSpeed'],
        "_noteJumpStartBeatOffset": item['_difficultyBeatmaps'][0]['_noteJumpStartBeatOffset'],
        "_beatmapData": {
            "FileID": 0,
            "PathID": pidDifficultyObjects[0]
        },
        "ByteSize": 36
    } for item in out["_difficultyBeatmapSets"]
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
            "PathID": pidAudioClip
        },
        "_beatsPerMinute": out['_beatsPerMinute'],
        "_songTimeOffset": out['_songTimeOffset'],
        "_shuffle": out['_shuffle'],
        "_shufflePeriod": out['_shufflePeriod'],
        "_previewStartTime": out['_previewStartTime'],
        "_previewDuration": out['_previewDuration'],
        "_coverImageTexture2D": {
            "FileID": 0,
            "PathID": 9
        },
        "_environmentSceneInfo": {
            "FileID": 0,
            "PathID": 252
        },
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
                    "ByteSize": sum([item['ByteSize'] for item in arr])
                }
            ]
        }
    }
}

a['Metadata'] = {
    "TypeID": 15
}

with open(levelDat, 'wb') as fs:
    levelData.writeBeatmapLevel(fs, a['Data'])

with open(levelDat, 'rb') as fs:
    size = len(fs.read())
    fs.seek(0)
    serialize(levelData.readBeatmapLevel(fs), levelJson)

size = size + (4 - size) % 4
print("Calculated ByteSize: " + str(size))
a['Metadata']['ByteSize'] = size

serialize(a, levelJson)

objects = [audioClipObjPath, o, levelJson]

print("Created Objects: " + str(objects))
print("With PIDs: " + str(pidAudioClip) + ", " + str(pidDifficultyObjects[0])+ ", " + str("?"))

asset = replacer.getAsset(asset_path)

for item in objects:
    d = deserialize(item)
    replacer.addObject(asset, d['Data'], d['Metadata'])

replacer.findData(asset, json_out_dir)

# Edit ExtrasLevelCollection to add song

j = deserialize(os.path.join(json_out_dir, os.path.join("LevelCollections", "ExtrasLevelCollection.json")))
lev = deserialize(os.path.join(json_out_dir, os.path.join("SongLevels", n + ".json")))

j['_beatmapLevels']['size'] += 1

levelPtr = {
    "data": {
        "FileID": 0,
        "PathID": lev['PathID']
    },
    "ByteSize": 12
},

j['_beatmapLevels']['Array'].append(levelPtr)

serialize(j, os.path.join(json_out_dir, os.path.join("LevelCollections", "ExtrasLevelCollection.json")))

if '.split' in asset_path:
    asset_path = asset_path.split('.split')[0]
    assert asset_path.endswith('.assets'), ".split file must have .assets immediately before .split!"
replacer.saveAsset(asset, output, asset_path)

replacer.findData(replacer.getAsset(output), json_out_dir)