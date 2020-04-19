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
		f.write(op + ' al, al\n')
		f.write(op + ' ah, ah\n')
		f.write(op + ' cl, cl\n')
		f.write(op + ' ch, ch\n')
		f.write(op + ' ax, bx\n')
		f.write(op + ' cx, dx\n')
		f.write(op + ' eax, ebx\n')
		f.write(op + ' ecx, edx\n')
	# ---------------------------------- op reg, mem ----------------------------------
	# op reg, [base]
	if case < 0 or case == 1:
		f.write(op + ' ax, [ebx + 0]\n')
		f.write(op + ' cx, [edx]\n')
		f.write(op + ' ebx, [eax]\n')
		f.write(op + ' esi, [42 + ecx + 0 - 21 * 2]\n')
		f.write(op + ' esi, [esp]\n')
		f.write(op + ' esi, [ebp]\n')
	# op reg, [disp]
	if case < 0 or case == 2:
		f.write(op + ' ax, [0x1]\n')
		f.write(op + ' al, [0x0]\n')
		f.write(op + ' cx, [0b10]\n')
		f.write(op + ' ebx, [10 - 20]\n')
		f.write(op + ' esi, [0x77]\n')
		f.write(op + ' esi, [0 - 0x1377]\n')
		f.write(op + ' esi, [0x13771999]\n')
	# op reg, [scale * index]
	if case < 0 or case == 3:
		f.write(op + ' ax, [eax * 2]\n')
		f.write(op + ' ax, [ebx * 2]\n')
		f.write(op + ' cx, [2 * edx]\n')
		f.write(op + ' ebx, [2 * eax * 2]\n')
		f.write(op + ' esi, [4 * ecx]\n')
		f.write(op + ' esi, [8 * ebp]\n')
	# op reg, [base + disp]
	if case < 0 or case == 4:
		f.write(op + ' ax, [ebx + 0x77]\n')
#		f.write(op + ' eax, [ebx + 0x99]\n')
		f.write(op + ' ebx, [ebx + 0x1999]\n')
		f.write(op + ' ch, [eax + 0x42]\n')
		f.write(op + ' ecx, [eax + 0x1234]\n')
		f.write(op + ' edx, [esp + 0xA]\n')
		f.write(op + ' al, [esp + 0xABCDE]\n')
		f.write(op + ' ah, [ebp + 0xB]\n')
		f.write(op + ' bl, [ebp + 0xA0C]\n')
	# op reg, [base + scale * index]
	if case < 0 or case == 5:
		f.write(op + ' ax, [ebx + ebx * 2]\n')
		f.write(op + ' cx, [ecx + 2 * edx]\n')
		f.write(op + ' ebx, [esp + 2 * eax * 2]\n')
		f.write(op + ' eax, [ebp + 4 * ecx]\n')
		f.write(op + ' ebx, [esp + 2 * 4 * ebp]\n')
		f.write(op + ' ecx, [ebp + ebp]\n')
		f.write(op + ' dx, [eax + ebp]\n')
		f.write(op + ' bp, [ebp + eax]\n')
		f.write(op + ' al, [ebp + esp]\n')
		f.write(op + ' ah, [eax + 8 * eax]\n')
	# op reg, [scale * index + disp]
	if case < 0 or case == 6:
		f.write(op + ' al, al\n')
	# op reg, [base + scale * index + disp]
	if case < 0 or case == 7:
		f.write(op + ' ax, [ebx + ebx * 2 + 0x42]\n')
		f.write(op + ' cx, [ecx + 2 * edx + 0xABCDE]\n')
		f.write(op + ' ebx, [0x42 - 0x77 + esp + 2 * eax * 2]\n')
		f.write(op + ' eax, [0x21 + ebp + 4 * ecx]\n')
		f.write(op + ' eax, [0x4221 + ebp + 4 * ecx]\n')
#		f.write(op + ' ebx, [esp + 0x99 + 2 * 4 * ebp]\n')
		f.write(op + ' ebx, [esp + 0x13771217 + 2 * 4 * ebp]\n')
		f.write(op + ' ecx, [ebp + ebp + 0xA]\n')
		f.write(op + ' ecx, [ebp + ebp + 0xAFF]\n')
		f.write(op + ' dx, [eax + 0b1010 - 0xA + ebp]\n')
		f.write(op + ' dx, [eax + ebp + 0xDAF]\n')
		f.write(op + ' bp, [ebp + 0b00111 * 3 - 2 + eax]\n')
		f.write(op + ' al, [ebp + 42 + 0x42 + esp]\n')
		f.write(op + ' ah, [eax + 8 * eax + 0b1001]\n')
	# ---------------------------------- op mem, reg ----------------------------------
	# op [base], reg
	if case < 0 or case == 8:
		f.write(op + ' [ebx + 0], ax\n')
		f.write(op + ' [edx], cx\n')
		f.write(op + ' [eax], ebx\n')
		f.write(op + ' [42 + ecx + 0 - 21 * 2], esi\n')
		f.write(op + ' [esp], ah\n')
		f.write(op + ' [ebp], ax\n')
	# op [disp], reg
	if case < 0 or case == 9:
		f.write(op + ' [0x1], ax\n')
		f.write(op + ' [0x0], al\n')
		f.write(op + ' [0b10], cx\n')
		f.write(op + ' [10 - 20], ebx\n')
		f.write(op + ' [0x77], esi\n')
		f.write(op + ' [0 - 0x1377], ax\n')
		f.write(op + ' [0x13771999], bl\n')
	# op [scale * index], reg
	if case < 0 or case == 10:
		f.write(op + ' [eax * 2], ax\n')
		f.write(op + ' [ebx * 2], ax\n')
		f.write(op + ' [2 * edx], cx\n')
		f.write(op + ' [2 * eax * 2], ebx\n')
		f.write(op + ' [4 * ecx], esi\n')
		f.write(op + ' [8 * ebp], esi\n')
	# op [base + disp], reg
	if case < 0 or case == 11:
		f.write(op + ' [ebx + 0x77], ax\n')
#		f.write(op + ' [ebx + 0x99], eax\n')
		f.write(op + ' [ebx + 0x1999], ebx\n')
		f.write(op + ' [eax + 0x42], ch\n')
		f.write(op + ' [eax + 0x1234], ecx\n')
		f.write(op + ' [esp + 0xA], edx\n')
		f.write(op + ' [esp + 0xABCDE], al\n')
		f.write(op + ' [ebp + 0xB], ah\n')
		f.write(op + ' [ebp + 0xA0C], bl\n')
	# op [base + scale * index], reg
	if case < 0 or case == 12:
		f.write(op + ' [ebx + ebx * 2], ax\n')
		f.write(op + ' [ecx + 2 * edx], cx\n')
		f.write(op + ' [esp + 2 * eax * 2], edx\n')
		f.write(op + ' [ebp + 4 * ecx], eax\n')
		f.write(op + ' [esp + 2 * 4 * ebp], ebx\n')
		f.write(op + ' [ebp + ebp], ecx\n')
		f.write(op + ' [eax + ebp], dx\n')
		f.write(op + ' [ebp + eax], bp\n')
		f.write(op + ' [ebp + esp], al\n')
		f.write(op + ' [eax + 8 * eax], ah\n')
	# op [scale * index + disp], reg
	if case < 0 or case == 13:
		f.write(op + ' al, al\n')
	# op [base + scale * index + disp], reg
	if case < 0 or case == 14:
		f.write(op + ' [ebx + ebx * 2 + 0x42], ax\n')
		f.write(op + ' [ecx + 2 * edx + 0xABCDE], cx\n')
		f.write(op + ' [0x42 - 0x77 + esp + 2 * eax * 2], ebx\n')
		f.write(op + ' [0x21 + ebp + 4 * ecx], eax\n')
		f.write(op + ' [0x4221 + ebp + 4 * ecx], eax\n')
#		f.write(op + ' [esp + 0x99 + 2 * 4 * ebp], ebx\n')
		f.write(op + ' [esp + 0x13771217 + 2 * 4 * ebp], ebx\n')
		f.write(op + ' [ebp + ebp + 0xA], ecx\n')
		f.write(op + ' [ebp + ebp + 0xAFF], ecx\n')
		f.write(op + ' [eax + 0b1010 - 0xA + ebp], dx\n')
		f.write(op + ' [eax + ebp + 0xDAF], dx\n')
		f.write(op + ' [ebp + 0b00111 * 3 - 2 + eax], bp\n')
		f.write(op + ' [ebp + 42 + 0x42 + esp], al\n')
		f.write(op + ' [eax + 8 * eax + 0b1001], ah\n')

	# ---------------------------------- op reg, imd ----------------------------------
	if case < 0 or case == 15:
		f.write(op + ' al, al\n')
	# op mem, imd
	# op  al, imd
	# op  ax, imd
	# op eax, imd

	# op 64-bits TODO

f.close()

