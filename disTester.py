import requests

import sys
import os

def testFile(fName, tName, detail = False):
	try:
		# read test
		primeArr = list(open(fName, 'rb').read())

		# DisAssemble
		stream = os.popen("python3 hDisAssembler.py " + fName)
		asm = stream.read()

		asmName = fName.split('.')
		if len(asmName) > 1:
			asmName = '.'.join(asmName[:-1])
		else:
			asmName = asmName[0]
		asmName = asmName + ".asm"
		asmName = "__" + asmName
		open(asmName, "w").write(asm)

		# Assemble Again
		stream = os.popen("python3 hAssembler.py " + asmName + " --raw")
		output = stream.read()
		newArr = output.split()
		newArr = list(map(eval, newArr))

		# Report
		if detail:
			print("Input:")
			print(list(map('{0:08b}'.format, primeArr)))
			print("\nOutput:")
			print(asm)
			print("Output Bytes:")
			print(list(map('{0:08b}'.format, newArr)))
			print("")

		if (primeArr == newArr):
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
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, reg")
	print("01.", end = ' ')
	os.system("python3 testGen.py 1")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [base]")
	print("02.", end = ' ')
	os.system("python3 testGen.py 2")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [disp]")
	print("03.", end = ' ')
	os.system("python3 testGen.py 3")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [scale * index]")
	print("04.", end = ' ')
	os.system("python3 testGen.py 4")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [base + disp]")
	print("05.", end = ' ')
	os.system("python3 testGen.py 5")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [base + scale * index]")
	print("06.", end = ' ')
	os.system("python3 testGen.py 6")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [scale * index + disp]")
	print("07.", end = ' ')
	os.system("python3 testGen.py 7")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [base + scale * index + disp]")
	print("08.", end = ' ')
	os.system("python3 testGen.py 8")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, [base + scale * index + disp] (64-bits)")
	print("09.", end = ' ')
	os.system("python3 testGen.py 9")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [base], reg")
	print("10.", end = ' ')
	os.system("python3 testGen.py 10")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [disp], reg")
	print("11.", end = ' ')
	os.system("python3 testGen.py 11")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [scale * index], reg")
	print("12.", end = ' ')
	os.system("python3 testGen.py 12")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [base + disp], reg")
	print("13.", end = ' ')
	os.system("python3 testGen.py 13")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [base + scale * index], reg")
	print("14.", end = ' ')
	os.system("python3 testGen.py 14")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [scale * index + disp], reg")
	print("15.", end = ' ')
	os.system("python3 testGen.py 15")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [base + scale * index + disp], reg")
	print("16.", end = ' ')
	os.system("python3 testGen.py 16")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op [base + scale * index + disp], reg (64-bits)")
	print("17.", end = ' ')
	os.system("python3 testGen.py 17")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg, imd")
	print("18.", end = ' ')
	os.system("python3 testGen.py 18")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op (al | ax | eax | rax), imd")
	print("19.", end = ' ')
	os.system("python3 testGen.py 19")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op mem, imd")
	print("20.", end = ' ')
	os.system("python3 testGen.py 20")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op reg")
	print("21.", end = ' ')
	os.system("python3 testGen.py 21")
	os.system("python3 disTestGen.py testGened.asm")
	testFile("testGened.bin", "op mem")
