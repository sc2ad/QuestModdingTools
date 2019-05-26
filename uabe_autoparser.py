# Auto-creates a to_from file using the UABE json/text data.

import argparse
import json

imports = """import struct
import json
import argparse

from helper import *

"""

auto = """### This file was auto-generated using uabe_autoparser.py
### Author: Sc2ad
"""

activation = """if __name__ == '__main__':
\tparser = argparse.ArgumentParser(description="Provides a converter for BeatmapLevelData from .dat files (exported from UABE)")
\tparser.add_argument("file", type=str, help="The .dat file to load.")
\tparser.add_argument('--output', type=str, help="The output directory for the serialized json.")
\tparser.add_argument('--load', type=str, help="Will use the provided file in order to load the updates to the .dat file.")

\targs = parser.parse_args()

\tif args.load:
\t\tdat = deserialize(args.load)
\t\tprint("Deserialized: " + str(dat))
\t\t# Write the changes to the file.
\t\twith open(args.file, "wb") as f:
"""

activation2 = """
\telse:
\t\twith open(args.file, "rb") as f:
"""

activation3 = """
\t\t\tprint(dat)
\t\t\tif args.output:
\t\t\t\tserialize(dat, args.output)
\t\t\t\tprint("Serialized!")"""

def getType(s):
    if s == "string":
        return "AlignedString"
    elif s == "int":
        return "Int32"
    elif s == "float":
        return "Float"
    elif s == "bool":
        return "Bool"
    elif s.startswith("PPtr<"):
        return "Ptr"
    elif s == "SInt64":
        return "Int64"
    elif s == "vector":
        return "Vector"
    else:
        return s


def load(fs):
    o = {}
    d = json.load(fs)
    o['name'] = next(iter(d.keys())).split(" ")[1]
    o['subs'] = []
    m = d[next(iter(d.keys()))]
    for k in m.keys():
        spl = k.split(" ")
        if spl[2].startswith("m_"):
            spl[2] = spl[2][2:]
        typ = getType(spl[1])
        
        if type(m[k]) == dict:
            if typ == "Vector" or typ == "Ptr":
                o[spl[2]] = typ
                continue
            o2 = {}
            o2['name'] = spl[1]
            for k2 in m[k].keys():
                spl2 = k2.split(" ")
                if spl2[2].startswith("m_"):
                    spl2[2] = spl2[2][2:]
                typ2 = getType(spl2[1])
                o2[spl2[2]] = typ2
            o['subs'].append(o2)
        
        o[spl[2]] = typ
    return o

def createRead(fs, item):
    fs.write("def read" + item['name'] + "(fs):\n")
    fs.write("\to = {}\n")
    for k in item.keys():
        if k != 'name':
            fs.write("\to['" + k + "'] = read" + item[k] + "(fs)\n")
    fs.write("\treturn o\n")

def createWrite(fs, item):
    fs.write("def write" + item['name'] + "(fs, o):\n")
    for k in item.keys():
        if k != 'name':
            fs.write("\twrite" + item[k] + "(fs, o['" + k + "'])\n")
    fs.write("\n")

def createMainRead(fs, data):
    fs.write("def read" + data['name'] + "(fs):\n")
    fs.write("\to = {}\n")
    for k in data.keys():
        if k != "name" and k != "subs":
            fs.write("\to['" + k + "'] = read" + data[k] + "(fs)\n")
    fs.write("\treturn o\n")

def createMainWrite(fs, data):
    fs.write("def write" + data['name'] + "(fs, o):\n")
    for k in data.keys():
        if k != 'name' and k != "subs":
            fs.write("\twrite" + data[k] + "(fs, o['" + k + "'])\n")
    fs.write("\n")

def createActivation(fs, data):
    fs.write(activation)
    fs.write("\t\t\twrite" + data['name'] + "(f, dat)\n")
    fs.write(activation2)
    fs.write("\t\t\tdat = read" + data['name'] + "(f)\n")
    fs.write(activation3)

def create(data):
    with open(data['name'][0].lower() + data['name'][1:len(data['name'])] + "_to_from_UABE.py", "w") as fs:
        fs.write(imports)
        fs.write(auto)
        for item in data['subs']:
            createRead(fs, item)
            createWrite(fs, item)
        createMainRead(fs, data)
        createMainWrite(fs, data)
        createActivation(fs, data)
        fs.write("\n")
    print("Created program!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automatically generates .py files that can convert to/from UABE binary data and JSONs.")
    parser.add_argument("file", type=str, help="The JSON file to build this script out of.")

    args = parser.parse_args()

    with open(args.file.strip(), 'r') as inp:
        a = load(inp)
        print("Loaded: " + str(a))
        create(a)