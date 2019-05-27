import struct
import json
import argparse

from helper import *

### This file was auto-generated using uabe_autoparser.py
### Author: Sc2ad
def readStreamedResource(fs):
	o = {}
	o['Source'] = readAlignedString(fs)
	o['Offset'] = readUInt64(fs)
	o['Size'] = readUInt64(fs)
	return o
def writeStreamedResource(fs, o):
	writeAlignedString(fs, o['Source'])
	writeUInt64(fs, o['Offset'])
	writeUInt64(fs, o['Size'])

def readAudioClip(fs):
	o = {}
	o['Name'] = readAlignedString(fs)
	o['LoadType'] = readInt32(fs)
	o['Channels'] = readInt32(fs)
	o['Frequency'] = readInt32(fs)
	o['BitsPerSample'] = readInt32(fs)
	o['Length'] = readFloat(fs)
	# Throwaway
	o['IsTrackerFormat'] = readBool(fs)
	readAlign(fs, fs.tell())
	o['Ambisonic'] = readBool(fs)
	o['SubsoundIndex'] = readInt32(fs)
	o['PreloadAudioData'] = readBool(fs)
	o['LoadInBackground'] = readBool(fs)
	o['Legacy3D'] = readBool(fs)
	readAlign(fs, fs.tell())
	o['Resource'] = readStreamedResource(fs)
	o['CompressionFormat'] = readInt32(fs)
	return o
def writeAudioClip(fs, o):
	writeAlignedString(fs, o['Name'])
	writeInt32(fs, o['LoadType'])
	writeInt32(fs, o['Channels'])
	writeInt32(fs, o['Frequency'])
	writeInt32(fs, o['BitsPerSample'])
	writeFloat(fs, o['Length'])
	writeBool(fs, o['IsTrackerFormat'])
	writeAlign(fs, fs.tell())
	writeBool(fs, o['Ambisonic'])
	writeInt32(fs, o['SubsoundIndex'])
	writeBool(fs, o['PreloadAudioData'])
	writeBool(fs, o['LoadInBackground'])
	writeBool(fs, o['Legacy3D'])
	writeAlign(fs, fs.tell())
	writeStreamedResource(fs, o['Resource'])
	writeInt32(fs, o['CompressionFormat'])

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
			writeAudioClip(f, dat)

	else:
		with open(args.file, "rb") as f:
			dat = readAudioClip(f)

			print(dat)
			if args.output:
				serialize(dat, args.output)
				print("Serialized!")
