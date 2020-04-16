# Assembler Program in Python
# By Kamyar Mirzavaziri
import sys
from instruction import Instruction

def read():
	if len(sys.argv) < 2:
		raise Exception("No File Specified!")
	return open(sys.argv[1], 'r')

def write(bits): # TODO
	OutputFile = open("a.out", "wb")
	OutputFile.write(bytes)

def assemble(assemblyFile):
	bytes = []
	for line in assemblyFile:
		splitedLine = line.split()
		if len(splitedLine) < 1:
			continue
		head = splitedLine[0]
		if len(head) < 1 or head[0] == '#':
			continue
		tail = line[len(head):]
		try:
			bytes += Instruction(head, tail).toMachineCode()
		except Exception as e:
			print(e)
	return bytearray(bytes)

try:
	assemblyFile = read()
	bytes = assemble(assemblyFile)
	print(list(map(hex, bytes)))
except Exception as e:
	print(e)

