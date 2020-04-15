# Assembler Program in Python
# By Kamyar Mirzavaziri
import sys

if len(sys.argv) < 2:
	raise Exception('No File Specified!');

assemblyFile = sys.argv[1]

file = open(assemblyFile, "r")

for line in file:
	print (line)
