import struct
import json
import argparse

from helper import *

### This file was auto-generated using uabe_autoparser.py
### Author: Sc2ad
def readGLTextureSettings(fs):
	o = {}
	o['FilterMode'] = readInt32(fs)
	o['Aniso'] = readInt32(fs)
	o['MipBias'] = readFloat(fs)
	o['WrapU'] = readInt32(fs)
	o['WrapV'] = readInt32(fs)
	o['WrapW'] = readInt32(fs)
	return o
def writeGLTextureSettings(fs, o):
	writeInt32(fs, o['FilterMode'])
	writeInt32(fs, o['Aniso'])
	writeFloat(fs, o['MipBias'])
	writeInt32(fs, o['WrapU'])
	writeInt32(fs, o['WrapV'])
	writeInt32(fs, o['WrapW'])

def readStreamingInfo(fs):
	o = {}
	o['Offset'] = readUInt32(fs)
	o['Size'] = readUInt32(fs)
	o['Path'] = readAlignedString(fs)
	return o
def writeStreamingInfo(fs, o):
	writeUInt32(fs, o['Offset'])
	writeUInt32(fs, o['Size'])
	writeAlignedString(fs, o['Path'])

def readTypelessData(fs):
	o = {}
	o['size'] = readUInt32(fs)
	o['Data'] = readHex(fs, o['size'])
	return o
def writeTypelessData(fs, o):
	writeUInt32(fs, o['size'])
	writeHex(fs, o['Data'])

def readTexture2D(fs):
	o = {}
	o['Name'] = readAlignedString(fs)
	o['ForcedFallbackFormat'] = readInt32(fs)
	o['DownscaleFallback'] = readBool(fs)
	readAlign(fs, fs.tell())
	o['Width'] = readInt32(fs)
	o['Height'] = readInt32(fs)
	o['CompleteImageSize'] = readInt32(fs)
	o['TextureFormat'] = readInt32(fs)
	o['MipCount'] = readInt32(fs)
	o['IsReadable'] = readBool(fs)
	o['StreamingMipmaps'] = readBool(fs)
	readAlign(fs, fs.tell())
	o['StreamingMipmapsPriority'] = readInt32(fs)
	o['ImageCount'] = readInt32(fs)
	o['TextureDimension'] = readInt32(fs)
	o['TextureSettings'] = readGLTextureSettings(fs)
	o['LightmapFormat'] = readInt32(fs)
	o['ColorSpace'] = readInt32(fs)
	o['image'] = readTypelessData(fs)
	o['StreamData'] = readStreamingInfo(fs)
	return o
def writeTexture2D(fs, o):
	writeAlignedString(fs, o['Name'])
	writeInt32(fs, o['ForcedFallbackFormat'])
	writeBool(fs, o['DownscaleFallback'])
	writeAlign(fs, fs.tell())
	writeInt32(fs, o['Width'])
	writeInt32(fs, o['Height'])
	writeInt32(fs, o['CompleteImageSize'])
	writeInt32(fs, o['TextureFormat'])
	writeInt32(fs, o['MipCount'])
	writeBool(fs, o['IsReadable'])
	writeBool(fs, o['StreamingMipmaps'])
	writeAlign(fs, fs.tell())
	writeInt32(fs, o['StreamingMipmapsPriority'])
	writeInt32(fs, o['ImageCount'])
	writeInt32(fs, o['TextureDimension'])
	writeGLTextureSettings(fs, o['TextureSettings'])
	writeInt32(fs, o['LightmapFormat'])
	writeInt32(fs, o['ColorSpace'])
	writeTypelessData(fs, o['image'])
	writeStreamingInfo(fs, o['StreamData'])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Provides a converter for BeatmapLevelData from .dat files (exported from UABE)")
	parser.add_argument("file", type=str, help="The .dat file to load.")
	parser.add_argument('--output', type=str, help="The output directory for the serialized json.")
	parser.add_argument('--load', type=str, help="Will use the provided file in order to load the updates to the .dat file.")

	args = parser.parse_args()

	if args.load:
		dat = deserialize(args.load)
		print("Deserialized: " + str(dat))
		# Write the changes to the file.
		with open(args.file, "wb") as f:
			writeTexture2D(f, dat)

	else:
		with open(args.file, "rb") as f:
			dat = readTexture2D(f)

			# print(dat)
			if args.output:
				serialize(dat, args.output)
				print("Serialized!")
