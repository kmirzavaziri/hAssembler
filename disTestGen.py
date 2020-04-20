import os
import sys

if len(sys.argv) < 2:
	print("No file specified!\nRight usage: python3 DisTestGen.py test.asm")

else:
	stream = os.popen("python3 hAssembler.py " + sys.argv[1] + " --raw")
	output = stream.read()
	arr = output.split()
	arr = list(map(eval, arr))
	binName = sys.argv[1].split('.')
	if len(binName) > 1:
		binName = '.'.join(binName[:-1])
	else:
		binName = binName[0]
	binName = binName + ".bin"
	open(binName, "wb").write(bytes(arr))

