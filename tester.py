import requests

import sys
import os

def testFile(fName, tName, detail = False):
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
		if detail:
			print(list(map('{0:08b}'.format, arr)))

		# get hAssembler.py machine code
		stream = os.popen("python3 hAssembler.py " + fName + " --raw")
		output = stream.read()
		hArr = output.split()
		hArr = list(map(eval, hArr))
		if detail:
			print(list(map('{0:08b}'.format, hArr)))

		if (arr == hArr):
			print("Test", "'" + tName + "'", "passed!", sep = ' ')
		else:
			print("Test", "'" + tName + "'", "failed!", sep = ' ')
	except Exception as e:
			print("Test", "'" + tName + "'", "failed with exception:", e, sep = ' ')

if len(sys.argv) >= 2:
	testFile(sys.argv[1], sys.argv[1], True)
else:
	print("00.", end = ' ')
	os.system("python3 testGen.py 0")
	testFile("testGened.asm", "op reg, reg")
	print("01.", end = ' ')
	os.system("python3 testGen.py 1")
	testFile("testGened.asm", "op reg, [base]")
	print("02.", end = ' ')
	os.system("python3 testGen.py 2")
	testFile("testGened.asm", "op reg, [disp]")
	print("03.", end = ' ')
	os.system("python3 testGen.py 3")
	testFile("testGened.asm", "op reg, [scale * index]")
	print("04.", end = ' ')
	os.system("python3 testGen.py 4")
	testFile("testGened.asm", "op reg, [base + disp]")
	print("05.", end = ' ')
	os.system("python3 testGen.py 5")
	testFile("testGened.asm", "op reg, [base + scale * index]")
	print("06.", end = ' ')
	os.system("python3 testGen.py 6")
	testFile("testGened.asm", "op reg, [scale * index + disp]")
	print("07.", end = ' ')
	os.system("python3 testGen.py 7")
	testFile("testGened.asm", "op reg, [base + scale * index + disp]")
	print("08.", end = ' ')
	os.system("python3 testGen.py 8")
	testFile("testGened.asm", "op reg, [base + scale * index + disp] (64-bits)")
	print("09.", end = ' ')
	os.system("python3 testGen.py 9")
	testFile("testGened.asm", "op [base], reg")
	print("10.", end = ' ')
	os.system("python3 testGen.py 10")
	testFile("testGened.asm", "op [disp], reg")
	print("11.", end = ' ')
	os.system("python3 testGen.py 11")
	testFile("testGened.asm", "op [scale * index], reg")
	print("12.", end = ' ')
	os.system("python3 testGen.py 12")
	testFile("testGened.asm", "op [base + disp], reg")
	print("13.", end = ' ')
	os.system("python3 testGen.py 13")
	testFile("testGened.asm", "op [base + scale * index], reg")
	print("14.", end = ' ')
	os.system("python3 testGen.py 14")
	testFile("testGened.asm", "op [scale * index + disp], reg")
	print("15.", end = ' ')
	os.system("python3 testGen.py 15")
	testFile("testGened.asm", "op [base + scale * index + disp], reg")
	print("16.", end = ' ')
	os.system("python3 testGen.py 16")
	testFile("testGened.asm", "op [base + scale * index + disp], reg (64-bits)")
	print("17.", end = ' ')
	os.system("python3 testGen.py 17")
	testFile("testGened.asm", "op reg, imd")
	print("18.", end = ' ')
	os.system("python3 testGen.py 18")
	testFile("testGened.asm", "op (al | ax | eax | rax), imd")
	print("19.", end = ' ')
	os.system("python3 testGen.py 19")
	testFile("testGened.asm", "op mem, imd")
	print("20.", end = ' ')
	os.system("python3 testGen.py 20")
	testFile("testGened.asm", "op reg")
	print("21.", end = ' ')
	os.system("python3 testGen.py 21")
	testFile("testGened.asm", "op mem")



