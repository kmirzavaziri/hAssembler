import requests

import sys
import os

from instruction import Instruction

def read():
	if len(sys.argv) < 2:
		raise Exception("No file specified!\nRight usage: python3 tester.py test.asm")
	if len(sys.argv) > 2:
		raise Exception("Too many files specified!")
	return open(sys.argv[1], 'r')

try:
	# read test
	assemblyFile = read()
	instructions = ""

	for line in assemblyFile:
		line = line.strip()
		if len(line) < 1 or line[0] == '#':
			continue
		instructions += "\r\n" + line

	# get site machine code
	url = 'https://defuse.ca/online-x86-assembler.htm'
	data = {'instructions': instructions, 'arch': 'x64', 'submit': 'Assemble'}
	rawPage = requests.post(url, data = data).text
	arrIndex = rawPage.find("Array Literal:")
	arrStart = rawPage.find("{", arrIndex)
	arrEnd = rawPage.find("}", arrIndex)
	arr = rawPage[arrStart+1:arrEnd].split(",")
	arr = list(map(eval, arr))
	print(arr)

	# get hAssembler.py machine code
	stream = os.popen("python3 hAssembler.py " + sys.argv[1] + " --raw")
	output = stream.read()
	hArr = output.split()
	hArr = list(map(eval, hArr))
	print(hArr)

	if (arr == hArr):
		print("Nailed it!")
	else:
		print("Awww...! couldn't match")
except Exception as e:
	print(e)
