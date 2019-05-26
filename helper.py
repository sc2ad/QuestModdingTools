import struct
import json

def read(fs, n):
    return fs.read(n)

def write(fs, data):
    return fs.write(data)

def write0(fs, n):
    return fs.write(b''.join([b'\x00' for i in range(n)]))

def readAlignedString(fs):
    length = readUInt32(fs)
    i = 0
    s = ""
    if length == 0:
        return ""
    while i < length:
        item = read(fs, 1)
        if item == b'\x00':
            continue
        s += item.decode()
        i += 1
    readAlign(fs, i)
    return s

def readAlign(fs, offset):
    read(fs, (4 - offset) % 4)

def writeAlignedString(fs, st):
    writeUInt32(fs, len(st))
    if len(st) == 0:
        return
    for i in range(len(st)):
        write(fs, bytes([ord(st[i])]))
    writeAlign(fs, i + 1)

def writeAlign(fs, offset):
    write0(fs, (4 - offset % 4))

def readBool(fs):
    return struct.unpack("?", read(fs, 1))[0]

def writeBool(fs, bol):
    write(fs, struct.pack("?", bol))

def readUInt8(fs):
    return struct.unpack("B", read(fs, 1))[0]

def writeUInt8(fs, integer):
    write(fs, struct.pack("B", integer))

def readInt32(fs):
    return struct.unpack("i", read(fs, 4))[0]

def writeInt32(fs, integer):
    write(fs, struct.pack("i", integer))

def readUInt32(fs):
    return struct.unpack("I", read(fs, 4))[0]

def writeUInt32(fs, integer):
    write(fs, struct.pack("I", integer))

def readFloat(fs):
    return struct.unpack("f", read(fs, 4))[0]

def writeFloat(fs, flt):
    write(fs, struct.pack("f", flt))

def readUInt64(fs):
    return struct.unpack("Q", read(fs, 8))[0]

def writeUInt64(fs, integer):
    write(fs, struct.pack("Q", integer))

def readInt64(fs):
    return struct.unpack("q", read(fs, 8))[0]

def writeInt64(fs, integer):
    write(fs, struct.pack("q", integer))

def readPtr(fs):
    d = {}
    d['FileID'] = readInt32(fs)
    d['PathID'] = readInt64(fs)
    return d

def writePtr(fs, ptr):
    writeInt32(fs, ptr['FileID'])
    writeInt64(fs, ptr['PathID'])

def serialize(o, p):
    with open(p, "w") as f:
        json.dump(o, f, skipkeys=True, indent=4)

def deserialize(p):
    with open(p, 'r') as f:
        return json.load(f)