# Assembler Program in Python
# By Kamyar Mirzavaziri
import sys
from instruction import Instruction

def read():
	if len(sys.argv) < 2:
		raise Exception('No File Specified!');
	return open(sys.argv[1], 'r')

def write(bits): # TODO
	OutputFile = open("a.out", "wb")
	OutputFile.write(bytes)

def semiLex(assemblyFile):
	instructions = []
	for line in assemblyFile:
		splitedLine = line.split()
		if len(splitedLine) < 1:
			continue
		head = splitedLine[0]
		if len(head) < 1:
			continue
		data = line[len(head):]
		instructions.append(Instruction(head, data))
	return instructions

def assemble(instructions):
	bits = []
	for instruction in instructions:
		try:
			bits.append(instruction.toMachineCode())
		except Exception as e:
			print(e)
	return bits

try:
	assemblyFile = read()
	instructions = semiLex(assemblyFile)
	bits = assemble(instructions)
	print(bits)
except Exception as e:
	print(e)

