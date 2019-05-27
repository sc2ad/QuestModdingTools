import struct
import json
import argparse

from helper import *

### This file was auto-generated using uabe_autoparser.py
### Author: Sc2ad
def readMonoBehaviour(fs, obj={}):
	o = {}
	o['GameObject'] = obj["GameObject"] if "GameObject" in obj.keys() else readPtr(f)
	o['Enabled'] = obj["Enabled"] if "Enabled" in obj.keys() else readUInt32(f)
	o['MonoScript'] = obj["MonoScript"] if "MonoScript" in obj.keys() else readPtr(f)
	o['Name'] = obj["Name"] if "Name" in obj.keys() else readAlignedString(f)
	o['_jsonData'] = readAlignedString(fs)
	o['_signatureBytes'] = readVector(fs)
	o['_projectedData'] = readVector(fs)
	return o
def writeMonoBehaviour(fs, o):
	writePtr(fs, o['GameObject'])
	writeUInt8(fs, o['Enabled'])
	writeAlign(fs, fs.tell())
	writePtr(fs, o['Script'])
	writeAlignedString(fs, o['Name'])
	writeAlignedString(fs, o['_jsonData'])
	writeVector(fs, o['_signatureBytes'])
	writeVector(fs, o['_projectedData'])

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
			writeMonoBehaviour(f, dat)

	else:
		with open(args.file, "rb") as f:
			dat = readMonoBehaviour(f)

			print(dat)
			if args.output:
				serialize(dat, args.output)
				print("Serialized!")
