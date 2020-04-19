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
	"test",
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
		f.write(op + ' rax, rbx\n')
		f.write(op + ' rcx, rdx\n')
	# ---------------------------------- op reg, mem ----------------------------------
	# op reg, [base]
	if case < 0 or case == 1:
		f.write(op + ' ax, [ebx + 0]\n')
		f.write(op + ' cx, [edx]\n')
		f.write(op + ' ebx, [eax]\n')
		f.write(op + ' esi, [42 + ecx + 0 - 21 * 2]\n')
		f.write(op + ' esi, [esp]\n')
		f.write(op + ' esi, [ebp]\n')
		# 64-bits
		f.write(op + ' ebx, [rax]\n')
		f.write(op + ' rdx, [ebx + 0]\n')
		f.write(op + ' cx, [rdx]\n')
		f.write(op + ' rbx, [eax]\n')
		f.write(op + ' esi, [42 + rcx + 0 - 21 * 2]\n')
		f.write(op + ' esi, [esp]\n')
		f.write(op + ' esi, [rsp]\n')
		f.write(op + ' rsi, [esp]\n')
		f.write(op + ' rsi, [rbp]\n')
	# op reg, [disp]
	if case < 0 or case == 2:
		f.write(op + ' ax, [0x1]\n')
		f.write(op + ' al, [0x0]\n')
		f.write(op + ' cx, [0b10]\n')
		f.write(op + ' ebx, [10 - 20]\n')
		f.write(op + ' esi, [0x77]\n')
		f.write(op + ' esi, [0 - 0x1377]\n')
		f.write(op + ' esi, [0x13771999]\n')
		# 64-bits
		f.write(op + ' rax, [0x1]\n')
		f.write(op + ' rbx, [0x1000 - 0x2000]\n')
		f.write(op + ' rsi, [0x99]\n')
	# op reg, [scale * index]
	if case < 0 or case == 3:
		f.write(op + ' ax, [eax * 2]\n')
		f.write(op + ' ax, [ebx * 2]\n')
		f.write(op + ' cx, [2 * edx]\n')
		f.write(op + ' ebx, [2 * eax * 2]\n')
		f.write(op + ' esi, [4 * ecx]\n')
		f.write(op + ' esi, [8 * ebp]\n')
		# 64-bits
		f.write(op + ' ax, [rax * 2]\n')
		f.write(op + ' ax, [rbx * 2]\n')
		f.write(op + ' cx, [2 * rdx]\n')
		f.write(op + ' rbx, [2 * rax * 2]\n')
		f.write(op + ' rsi, [4 * rcx]\n')
		f.write(op + ' rsi, [8 * rbp]\n')
	# op reg, [base + disp]
	if case < 0 or case == 4:
		f.write(op + ' ax, [ebx + 0x42]\n')
		f.write(op + ' eax, [ebx + 0x99]\n')
		f.write(op + ' eax, [ebx + 0 - 0x99]\n')
		f.write(op + ' eax, [ebx + 0 - 0x42]\n')
		f.write(op + ' ebx, [ebx + 0x1999]\n')
		f.write(op + ' ch, [eax + 0x42135678]\n')
		f.write(op + ' ecx, [eax + 0x1234]\n')
		f.write(op + ' edx, [esp + 0xA]\n')
		f.write(op + ' al, [esp + 0xABCDE]\n')
		f.write(op + ' ah, [ebp + 0xB]\n')
		f.write(op + ' bl, [ebp + 0xA0C]\n')
		# 64-bits
		f.write(op + ' ax, [rbx + 0x42]\n')
		f.write(op + ' rax, [rbx + 0x99]\n')
		f.write(op + ' rax, [ebx + 0 - 0x99]\n')
		f.write(op + ' ecx, [rax + 0x1234]\n')
		f.write(op + ' rcx, [rsp + 0xA]\n')
		f.write(op + ' al, [rsp + 0xABCDE]\n')
		f.write(op + ' rdx, [rbp + 0xB]\n')
		f.write(op + ' bl, [rbp + 0xA0C]\n')
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
		# 64-bits
		f.write(op + ' ax, [rbx + rbx * 2]\n')
		f.write(op + ' cx, [rcx + 2 * rdx]\n')
		f.write(op + ' rbx, [rsp + 2 * rax * 2]\n')
		f.write(op + ' eax, [rbp + 4 * rcx]\n')
		f.write(op + ' rbx, [rsp + 2 * 4 * rbp]\n')
		f.write(op + ' ecx, [rbp + rbp]\n')
		f.write(op + ' dx, [rax + rbp]\n')
		f.write(op + ' bp, [rbp + rax]\n')
		f.write(op + ' rdx, [rbp + rsp]\n')
		f.write(op + ' ah, [rax + 8 * rax]\n')
	# op reg, [scale * index + disp]
	if case < 0 or case == 6:
		f.write(op + ' ax, [eax * 2 + 7]\n')
		f.write(op + ' ax, [ebx * 2 + 0x77]\n')
		f.write(op + ' cx, [2 * edx + 0x99]\n')
		f.write(op + ' ebx, [2 * eax * 2 + 0x1999]\n')
		f.write(op + ' esi, [4 * ecx + 0x00 - 0x42]\n')
		f.write(op + ' esi, [8 * ebp + 0x00 - 0xBB]\n')
		# 64-bits
		f.write(op + ' ax, [rax * 2 + 0b0 - 0b1000000]\n')
		f.write(op + ' ax, [0x777 + rbx * 2 + 0x666]\n')
		f.write(op + ' cx, [2 * rdx + 0x66]\n')
		f.write(op + ' rbx, [2 * rax * 2 + 0b10]\n')
		f.write(op + ' rsi, [4 * rcx + 0x77]\n')
		f.write(op + ' rsi, [0x99 + 8 * rbp]\n')
	# op reg, [base + scale * index + disp]
	if case < 0 or case == 7:
		f.write(op + ' ax, [ebx + ebx * 2 + 0x42]\n')
		f.write(op + ' cx, [ecx + 2 * edx + 0xABCDE]\n')
		f.write(op + ' ebx, [0x42 - 0x77 + esp + 2 * eax * 2]\n')
		f.write(op + ' eax, [0x21 + ebp + 4 * ecx]\n')
		f.write(op + ' eax, [0x4221 + ebp + 4 * ecx]\n')
		f.write(op + ' ebx, [esp + 0x99 + 2 * 4 * ebp]\n')
		f.write(op + ' ebx, [esp + 0x13771217 + 2 * 4 * ebp]\n')
		f.write(op + ' ecx, [ebp + ebp + 0xA]\n')
		f.write(op + ' ecx, [ebp + ebp + 0xAFF]\n')
		f.write(op + ' dx, [eax + 0b1010 - 0xA + ebp]\n')
		f.write(op + ' dx, [eax + ebp + 0xDAF]\n')
		f.write(op + ' bp, [ebp + 0b00111 * 3 - 2 + eax]\n')
		f.write(op + ' al, [ebp + 42 + 0x42 + esp]\n')
		f.write(op + ' ah, [eax + 8 * eax + 0b1001]\n')
		# 64-bits
		f.write(op + ' ax, [rbx + rbx * 2 + 0x42]\n')
		f.write(op + ' rbx, [0x42 - 0x77 + rsp + 2 * rax * 2]\n')
		f.write(op + ' rax, [0x21 + rbp + 4 * rcx]\n')
		f.write(op + ' rax, [0x4221 + rbp + 4 * rcx]\n')
		f.write(op + ' ebx, [rsp + 0x99 + 2 * 4 * rbp]\n')
		f.write(op + ' dx, [rax + 0b1010 - 0xA + rbp]\n')
		f.write(op + ' dx, [rax + rbp + 0xDAF]\n')
		f.write(op + ' bp, [rsp + 0b00111 * 3 - 2 + rax]\n')
		f.write(op + ' al, [rbp + 42 + 0x42 + rsp]\n')
		f.write(op + ' ah, [rax + 8 * rax + 0b1001]\n')
	# ---------------------------------- op mem, reg ----------------------------------
	# op [base], reg
	if case < 0 or case == 8:
		f.write(op + ' [ebx + 0], ax\n')
		f.write(op + ' [edx], cx\n')
		f.write(op + ' [eax], ebx\n')
		f.write(op + ' [42 + ecx + 0 - 21 * 2], esi\n')
		f.write(op + ' [esp], ah\n')
		f.write(op + ' [ebp], ax\n')
		# 64-bits
		f.write(op + ' [rax], ebx\n')
		f.write(op + ' [ebx + 0], rdx\n')
		f.write(op + ' [rdx], rcx\n')
		f.write(op + ' [eax], rbx\n')
		f.write(op + ' [42 + rcx + 0 - 21 * 2], esi\n')
		f.write(op + ' [esp], esi\n')
		f.write(op + ' [rsp], esi\n')
		f.write(op + ' [esp], rsi\n')
		f.write(op + ' [rbp], rsi\n')
	# op [disp], reg
	if case < 0 or case == 9:
		f.write(op + ' [0x1], ax\n')
		f.write(op + ' [0x0], al\n')
		f.write(op + ' [0b10], cx\n')
		f.write(op + ' [10 - 20], ebx\n')
		f.write(op + ' [0x77], esi\n')
		f.write(op + ' [0 - 0x1377], ax\n')
		f.write(op + ' [0x13771999], bl\n')
		# 64-bits
		f.write(op + ' rax, [0x1]\n')
		f.write(op + ' rbx, [0x1000 - 0x2000]\n')
		f.write(op + ' rsi, [0x99]\n')
	# op [scale * index], reg
	if case < 0 or case == 10:
		f.write(op + ' [eax * 2], ax\n')
		f.write(op + ' [ebx * 2], ax\n')
		f.write(op + ' [2 * edx], cx\n')
		f.write(op + ' [2 * eax * 2], ebx\n')
		f.write(op + ' [4 * ecx], esi\n')
		f.write(op + ' [8 * ebp], esi\n')
		# 64-bits
		f.write(op + ' ax, [rax * 2]\n')
		f.write(op + ' ax, [rbx * 2]\n')
		f.write(op + ' cx, [2 * rdx]\n')
		f.write(op + ' rbx, [2 * rax * 2]\n')
		f.write(op + ' rsi, [4 * rcx]\n')
		f.write(op + ' rsi, [8 * rbp]\n')
	# op [base + disp], reg
	if case < 0 or case == 11:
		f.write(op + ' [ebx + 0x77], ax\n')
		f.write(op + ' [ebx + 0x99], eax\n')
		f.write(op + ' [ebx + 0x1999], ebx\n')
		f.write(op + ' [eax + 0x42], ch\n')
		f.write(op + ' [eax + 0x1234], ecx\n')
		f.write(op + ' [esp + 0xA], edx\n')
		f.write(op + ' [esp + 0xABCDE], al\n')
		f.write(op + ' [ebp + 0xB], ah\n')
		f.write(op + ' [ebp + 0xA0C], bl\n')
		# 64-bits
		f.write(op + ' [rbx + 0x42], ax\n')
		f.write(op + ' [rbx + 0x99], rax\n')
		f.write(op + ' [ebx + 0 - 0x99], rax\n')
		f.write(op + ' [rax + 0x1234], ecx\n')
		f.write(op + ' [rsp + 0xA], rcx\n')
		f.write(op + ' [rsp + 0xABCDE], al\n')
		f.write(op + ' [rbp + 0xB], rdx\n')
		f.write(op + ' [rbp + 0xA0C], bl\n')
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
		# 64-bits
		f.write(op + ' [rbx + rbx * 2], ax\n')
		f.write(op + ' [rcx + 2 * rdx], cx\n')
		f.write(op + ' [rsp + 2 * rax * 2], rbx\n')
		f.write(op + ' [rbp + 4 * rcx], eax\n')
		f.write(op + ' [rsp + 2 * 4 * rbp], rbx\n')
		f.write(op + ' [rbp + rbp], ecx\n')
		f.write(op + ' [rax + rbp], dx\n')
		f.write(op + ' [rbp + rax], bp\n')
		f.write(op + ' [rbp + rsp], rdx\n')
		f.write(op + ' [rax + 8 * rax], ah\n')
	# op [scale * index + disp], reg
	if case < 0 or case == 13:
		f.write(op + ' [eax * 2 + 7], ax\n')
		f.write(op + ' [ebx * 2 + 0x77], ax\n')
		f.write(op + ' [2 * edx + 0x99], cx\n')
		f.write(op + ' [2 * eax * 2 + 0x1999], ebx\n')
		f.write(op + ' [4 * ecx + 0x00 - 0x42], esi\n')
		f.write(op + ' [8 * ebp + 0x00 - 0xBB], esi\n')
		# 64-bits
		f.write(op + ' [rax * 2 + 0b0 - 0b1000000], ax\n')
		f.write(op + ' [0x777 + rbx * 2 + 0x666], ax\n')
		f.write(op + ' [2 * rdx + 0x66], cx\n')
		f.write(op + ' [2 * rax * 2 + 0b10], rbx\n')
		f.write(op + ' [4 * rcx + 0x77], rsi\n')
		f.write(op + ' [0x99 + 8 * rbp], rsi\n')
	# op [base + scale * index + disp], reg
	if case < 0 or case == 14:
		f.write(op + ' [ebx + ebx * 2 + 0x42], ax\n')
		f.write(op + ' [ecx + 2 * edx + 0xABCDE], cx\n')
		f.write(op + ' [0x42 - 0x77 + esp + 2 * eax * 2], ebx\n')
		f.write(op + ' [0x21 + ebp + 4 * ecx], eax\n')
		f.write(op + ' [0x4221 + ebp + 4 * ecx], eax\n')
		f.write(op + ' [esp + 0x99 + 2 * 4 * ebp], ebx\n')
		f.write(op + ' [esp + 0x13771217 + 2 * 4 * ebp], ebx\n')
		f.write(op + ' [ebp + ebp + 0xA], ecx\n')
		f.write(op + ' [ebp + ebp + 0xAFF], ecx\n')
		f.write(op + ' [eax + 0b1010 - 0xA + ebp], dx\n')
		f.write(op + ' [eax + ebp + 0xDAF], dx\n')
		f.write(op + ' [ebp + 0b00111 * 3 - 2 + eax], bp\n')
		f.write(op + ' [ebp + 42 + 0x42 + esp], al\n')
		# 64-bits
		f.write(op + ' [rbx + rbx * 2 + 0x42], ax\n')
		f.write(op + ' [0x42 - 0x77 + rsp + 2 * rax * 2], rbx\n')
		f.write(op + ' [0x21 + rbp + 4 * rcx], rax\n')
		f.write(op + ' [0x4221 + rbp + 4 * rcx], rax\n')
		f.write(op + ' [rsp + 0x99 + 2 * 4 * rbp], ebx\n')
		f.write(op + ' [rax + 0b1010 - 0xA + rbp], dx\n')
		f.write(op + ' [rax + rbp + 0xDAF], dx\n')
		f.write(op + ' [rsp + 0b00111 * 3 - 2 + rax], bp\n')
		f.write(op + ' [rbp + 42 + 0x42 + rsp], al\n')
		f.write(op + ' [rax + 8 * rax + 0b1001], ah\n')
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

