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
	# ---------------------------------- op reg, reg ----------------------------------
	if case < 0 or case == 0:
		f.write(op + ' al, al\r\n')
		f.write(op + ' ah, ah\r\n')
		f.write(op + ' cl, cl\r\n')
		f.write(op + ' ch, ch\r\n')
		f.write(op + ' ax, bx\r\n')
		f.write(op + ' cx, dx\r\n')
		f.write(op + ' eax, ebx\r\n')
		f.write(op + ' ecx, edx\r\n')
	# ---------------------------------- op reg, mem ----------------------------------
	# op reg, [base]
	if case < 0 or case == 1:
		f.write(op + ' ax, [ebx + 0]\r\n')
		f.write(op + ' cx, [edx]\r\n')
		f.write(op + ' ebx, [eax]\r\n')
		f.write(op + ' esi, [42 + ecx + 0 - 21 * 2]\r\n')
		f.write(op + ' esi, [esp]\r\n')
		f.write(op + ' esi, [ebp]\r\n')
	# op reg, [disp]
	if case < 0 or case == 2:
		f.write(op + ' ax, [0x1]\r\n')
		f.write(op + ' al, [0x0]\r\n')
		f.write(op + ' cx, [0b10]\r\n')
		f.write(op + ' ebx, [10 - 20]\r\n')
		f.write(op + ' esi, [0x77]\r\n')
		f.write(op + ' esi, [0 - 0x1377]\r\n')
		f.write(op + ' esi, [0x13771999]\r\n')
	# op reg, [scale * index]
	if case < 0 or case == 3:
		f.write(op + ' ax, [eax * 2]\r\n')
		f.write(op + ' ax, [ebx * 2]\r\n')
		f.write(op + ' cx, [2 * edx]\r\n')
		f.write(op + ' ebx, [2 * eax * 2]\r\n')
		f.write(op + ' esi, [4 * ecx]\r\n')
		f.write(op + ' esi, [8 * ebp]\r\n')
	# op reg, [base + disp]
	if case < 0 or case == 4:
		f.write(op + ' ax, [ebx + 0x77]\r\n')
#		f.write(op + ' eax, [ebx + 0x99]\r\n')
		f.write(op + ' ebx, [ebx + 0x1999]\r\n')
		f.write(op + ' ch, [eax + 0x42]\r\n')
		f.write(op + ' ecx, [eax + 0x1234]\r\n')
		f.write(op + ' edx, [esp + 0xA]\r\n')
		f.write(op + ' al, [esp + 0xABCDE]\r\n')
		f.write(op + ' ah, [ebp + 0xB]\r\n')
		f.write(op + ' bl, [ebp + 0xA0C]\r\n')
	# op reg, [base + scale * index]
	if case < 0 or case == 5:
		f.write(op + ' ax, [ebx + ebx * 2]\r\n')
		f.write(op + ' cx, [ecx + 2 * edx]\r\n')
		f.write(op + ' ebx, [esp + 2 * eax * 2]\r\n')
		f.write(op + ' eax, [ebp + 4 * ecx]\r\n')
		f.write(op + ' ebx, [esp + 2 * 4 * ebp]\r\n')
		f.write(op + ' ecx, [ebp + ebp]\r\n')
		f.write(op + ' dx, [eax + ebp]\r\n')
		f.write(op + ' bp, [ebp + eax]\r\n')
		f.write(op + ' al, [ebp + esp]\r\n')
		f.write(op + ' ah, [eax + 8 * eax]\r\n')
	# op reg, [scale * index + disp]
	if case < 0 or case == 6:
		f.write(op + ' al, al\r\n')
	# op reg, [base + scale * index + disp]
	if case < 0 or case == 7:
		f.write(op + ' ax, [ebx + ebx * 2 + 0x42]\r\n')
		f.write(op + ' cx, [ecx + 2 * edx + 0xABCDE]\r\n')
		f.write(op + ' ebx, [0x42 - 0x77 + esp + 2 * eax * 2]\r\n')
		f.write(op + ' eax, [0x21 + ebp + 4 * ecx]\r\n')
		f.write(op + ' eax, [0x4221 + ebp + 4 * ecx]\r\n')
#		f.write(op + ' ebx, [esp + 0x99 + 2 * 4 * ebp]\r\n')
		f.write(op + ' ebx, [esp + 0x13771217 + 2 * 4 * ebp]\r\n')
		f.write(op + ' ecx, [ebp + ebp + 0xA]\r\n')
		f.write(op + ' ecx, [ebp + ebp + 0xAFF]\r\n')
		f.write(op + ' dx, [eax + 0b1010 - 0xA + ebp]\r\n')
		f.write(op + ' dx, [eax + ebp + 0xDAF]\r\n')
		f.write(op + ' bp, [ebp + 0b00111 * 3 - 2 + eax]\r\n')
		f.write(op + ' al, [ebp + 42 + 0x42 + esp]\r\n')
		f.write(op + ' ah, [eax + 8 * eax + 0b1001]\r\n')
	# ---------------------------------- op mem, reg ----------------------------------
	# 8 - 14
	# ---------------------------------- op reg, imd ----------------------------------
	if case < 0 or case == 15:
		f.write(op + ' al, al\r\n')
	# op mem, imd
	# op  al, imd
	# op  ax, imd
	# op eax, imd

	# op 64-bits TODO

f.close()

