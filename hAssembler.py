# Assembler Program in Python
# by Kamyar Mirzavaziri

import sys

from instruction import Instruction

def read():
	if len(sys.argv) < 2:
		raise Exception("No file specified!\nRight usage: python3 hAssembler.py test.asm")
	return open(sys.argv[1], 'r')

def assemble(assemblyFile):
	currLineNo = 0
	instructions = []
	for line in assemblyFile:
		currLineNo += 1
		splitedLine = line.split()
		if len(splitedLine) < 1:
			continue
		head = splitedLine[0]
		if len(head) < 1 or head[0] == '#':
			continue
		tail = " ".join(splitedLine[1:])
		try:
			instruction = Instruction()
			instruction.fromAsm(head, tail)
			instructions.append(instruction)
		except Exception as e:
			print("Error on line ", currLineNo, ": ", e, sep = '')
	return instructions

try:
	assemblyFile = read()
	instructions = assemble(assemblyFile)
	if len(sys.argv) > 2 and sys.argv[2] == '--raw':
		for instruction in instructions:
			for byte in instruction.machineCode:
				print(byte, end = ' ')
	else:
		for instruction in instructions:
			print(instruction.toString())
except Exception as e:
	print(e)

