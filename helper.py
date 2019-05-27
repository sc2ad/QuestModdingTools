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

def readAlign(fs, offset, alignment=4):
    i = (alignment - offset) % alignment
    if i < offset:
        read(fs, i)

def writeAlignedString(fs, st):
    writeUInt32(fs, len(st))
    if len(st) == 0:
        return
    for i in range(len(st)):
        write(fs, bytes([ord(st[i])]))
    writeAlign(fs, i + 1)

def writeAlign(fs, offset, alignment=4):
    i = (alignment - offset) % alignment
    if i < offset:
        write0(fs, i)

def readCString(fs, align=True):
    s = ""
    start = fs.tell()
    while bytes([fs.peek()[0]]) != b'\x00':
        s += read(fs, 1).decode()
    if start == fs.tell():
        # Need to read one slot and realign
        # readAlign(fs, fs.tell())
        read(fs, 1)
        return s
    if align:
        readAlign(fs, fs.tell())
    return s

def writeCString(fs, s, align=True):
    start = fs.tell()
    for item in s:
        write(fs, item.encode())
    write0(fs, 1)
    if fs.tell() - start == 1:
        return
    if align:
        writeAlign(fs, fs.tell())

def readHex16(fs):
    orig = [hex(item) for item in read(fs, 16)]
    for i in range(len(orig)):
        if len(orig[i]) == 3:
            orig[i] = "0" + orig[i][2:]
        else:
            orig[i] = orig[i][2:]
    return ''.join(orig)

def writeHex16(fs, item):
    for i in range(0, len(item), 2):
        b = bytes([int(item[i] + item[i + 1], 16)])
        write(fs, b)

def readBool(fs):
    return struct.unpack("?", read(fs, 1))[0]

def writeBool(fs, bol):
    write(fs, struct.pack("?", bol))

def readUInt8(fs):
    return struct.unpack("B", read(fs, 1))[0]

def writeUInt8(fs, integer):
    write(fs, struct.pack("B", integer))

def readInt16(fs):
    return struct.unpack("h", read(fs, 2))[0]

def writeInt16(fs, integer):
    write(fs, struct.pack("h", integer))

def readUInt16(fs):
    return struct.unpack("H", read(fs, 2))[0]

def writeUInt16(fs, integer):
    write(fs, struct.pack("H", integer))

def readInt32(fs):
    return struct.unpack("i", read(fs, 4))[0]

def writeInt32(fs, integer):
    write(fs, struct.pack("i", integer))

def readUInt32(fs, prefix='<'):
    return struct.unpack(prefix + "I", read(fs, 4))[0]

def writeUInt32(fs, integer, prefix='<'):
    write(fs, struct.pack(prefix + "I", integer))

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

def readVector(fs):
    o = {}
    o['size'] = readUInt32(fs)
    o['Array'] = []
    for _ in range(o['size']):
        data = {"data": readUInt8(fs)}
        data['ByteSize'] = 1
        o['Array'].append(data)
    return o

def writeVector(fs, o):
    writeUInt32(fs, o['size'])
    for item in o['Array']:
        writeUInt8(fs, item['data'])

def serialize(o, p):
    with open(p, "w") as f:
        json.dump(o, f, skipkeys=True, indent=4)

def deserialize(p):
    with open(p, 'r') as f:
        return json.load(f)