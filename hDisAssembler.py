# DisAssembler Program in Python
# by Kamyar Mirzavaziri

import sys

from instruction import Instruction

def read():
	if len(sys.argv) < 2:
		raise Exception("No file specified!\nRight usage: python3 hDisAssembler.py test.bin")
	file = open(sys.argv[1], 'rb')
	return file.read()

def disAssemble(stream):
	instructions = []
	while stream != []:
		try:
			instruction = Instruction()
			stream = instruction.fromBin(stream)
			instructions.append(instruction)
		except Exception as e:
			print("Error on byte with content ", "{0:02X}".format(stream[0]), ": ",  e, sep = '')
			stream = stream[1:]
	return instructions

try:
	machineCode = list(read())
	instructions = disAssemble(machineCode)

	for instruction in instructions:
		print(instruction.assemblyCode)

except Exception as e:
	print(e)

