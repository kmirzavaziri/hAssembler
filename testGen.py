import sys

if len(sys.argv) < 2:
	case = -1
else:
	case = int(sys.argv[1])

f = open("testGened.asm", "w")

nBinO = [
	"add",
	"mov",
	"adc",
	"sub",
	"sbb",
	"and",
	"or",
	"xor",
	"cmp",
]

for op in nBinO:
	# op reg, reg
	if case < 0 or case == 0:
		f.write(op + ' al, al\r\n')
		f.write(op + ' ah, ah\r\n')
		f.write(op + ' cl, cl\r\n')
		f.write(op + ' ch, ch\r\n')
		f.write(op + ' ax, bx\r\n')
		f.write(op + ' cx, dx\r\n')
		f.write(op + ' eax, ebx\r\n')
		f.write(op + ' ecx, edx\r\n')
	# op reg, [base]
	if case < 0 or case == 1:
		f.write(op + ' ax, [(2 - 1) * ebx]\r\n')
		f.write(op + ' cx, [((3 + 1) - 3) * edx]\r\n')
		f.write(op + ' ebx, [eax]\r\n')
		f.write(op + ' esi, [42 + ecx + 0 - 21 * 2]\r\n')
		f.write(op + ' esi, [esp]\r\n')
		f.write(op + ' esi, [ebp]\r\n')
	# op reg, [disp]
	if case < 0 or case == 2:
		f.write(op + ' ax, [0x1]\r\n')
		f.write(op + ' cx, [0b10]\r\n')
		f.write(op + ' ebx, [10 - 20]\r\n')
		f.write(op + ' esi, [0x77]\r\n')
		f.write(op + ' esi, [0 - 0x1377]\r\n')
		f.write(op + ' esi, [0x13771999]\r\n')
	# op reg, [scale*index]
	if case < 0 or case == 3:
		f.write(op + ' ax, [ebx * 2]\r\n')
		f.write(op + ' cx, [2 * edx]\r\n')
		f.write(op + ' ebx, [2 * eax * 2]\r\n')
		f.write(op + ' esi, [4 * ecx]\r\n')
		f.write(op + ' esi, [8 * esp]\r\n')
		f.write(op + ' esi, [8 * ebp]\r\n')
	# op reg, [base + disp]
	if case < 0 or case == 4:
		f.write(op + ' ax, [ebx + 0x99]\r\n')
		f.write(op + ' ax, [ebx + 0x1999]\r\n')
		f.write(op + ' ax, [eax + 0x99]\r\n')
		f.write(op + ' ax, [eax + 0x1999]\r\n')
		f.write(op + ' ax, [esp + 0x99]\r\n')
		f.write(op + ' ax, [esp + 0x1999]\r\n')
		f.write(op + ' ax, [ebp + 0x99]\r\n')
		f.write(op + ' ax, [ebp + 0x1999]\r\n')
	# op mem, reg
	# op reg, imd
	# op mem, imd
	# op  al, imd
	# op  ax, imd
	# op eax, imd

	# op 64-bits TODO

f.close()

