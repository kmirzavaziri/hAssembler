import requests

import sys
import os

from instruction import Instruction

def testFile(fName, tName):
	try:
		# read test
		assemblyFile = open(fName, 'r')
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
		#print(arr)

		# get hAssembler.py machine code
		stream = os.popen("python3 hAssembler.py " + fName + " --raw")
		output = stream.read()
		hArr = output.split()
		hArr = list(map(eval, hArr))
		#print(hArr)

		if (arr == hArr):
			print("Test", tName, "passed!", sep = ' ')
		else:
			print("Test", tName, "failed!", sep = ' ')
	except Exception as e:
			print("Test", tName, "failed with exception:", e, sep = ' ')

if len(sys.argv) >= 2:
	testFile(sys.argv[1], sys.argv[1])
else:
	os.system("python3 testGen.py 0")
	testFile("testGened.asm", "op reg, reg")
	os.system("python3 testGen.py 1")
	testFile("testGened.asm", "op reg, [base]")
	os.system("python3 testGen.py 2")
	testFile("testGened.asm", "op reg, [disp]")
	os.system("python3 testGen.py 3")
	testFile("testGened.asm", "op reg, [scale*index]")
	os.system("python3 testGen.py 4")
	testFile("testGened.asm", "op reg, [base + disp]")




