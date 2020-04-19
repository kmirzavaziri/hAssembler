# Tables
# by Kamyar Mirzavaziri
# Contains Operator Codes and Register Codes

# ----------------------------------------------- TABLE OF OP-CODES -----------------------------------------------
# coderr is the OpCode for following situations
#	op reg, reg
#	op reg, mem
#	op mem, reg
# codei is the OpCode for following situations
#	op reg, imd
#	op mem, imd
# codea is the OpCode for following situations
#	op  al, imd
#	op  ax, imd
#	op eax, imd
#	op rax, imd TODO
opCodes = {
	# normal binary
	"add" : {"ops": 2, "coder": 0b000000, "codei": 0b100000000, "codea": 0b000001, "name": "add" },
	"or"  : {"ops": 2, "coder": 0b000010, "codei": 0b100000001, "codea": 0b000011, "name": "or"  },
	"adc" : {"ops": 2, "coder": 0b000100, "codei": 0b100000010, "codea": 0b000101, "name": "adc" },
	"sbb" : {"ops": 2, "coder": 0b000110, "codei": 0b100000011, "codea": 0b000111, "name": "sbb" },
	"and" : {"ops": 2, "coder": 0b001000, "codei": 0b100000100, "codea": 0b001001, "name": "and" },
	"sub" : {"ops": 2, "coder": 0b001010, "codei": 0b100000101, "codea": 0b001011, "name": "sub" },
	"xor" : {"ops": 2, "coder": 0b001100, "codei": 0b100000110, "codea": 0b001101, "name": "xor" },
	"cmp" : {"ops": 2, "coder": 0b001110, "codei": 0b100000111, "codea": 0b001111, "name": "cmp" },
	"test": {"ops": 2, "coder": 0b100001, "codei": 0b111101000, "codea": 0b101010, "name": "test"}, # TODO
	"mov" : {"ops": 2, "coder": 0b100010, "codei": 0b1011     , "codea": 0b101100, "name": "mov" }, # mov alternate encoding
	# dec inc xchg xadd imul idiv bsf bsr stc clc std cld jmp jcc jcxz jecxz loop loope loopne shl shr neg not call ret syscall TODO
}

registers = {
	# 8-bits
	'al': {'size': 8, 'code': 0b000, "name": "al"},
	'cl': {'size': 8, 'code': 0b001, "name": "cl"},
	'dl': {'size': 8, 'code': 0b010, "name": "dl"},
	'bl': {'size': 8, 'code': 0b011, "name": "bl"},
	'ah': {'size': 8, 'code': 0b100, "name": "ah"},
	'ch': {'size': 8, 'code': 0b101, "name": "ch"},
	'dh': {'size': 8, 'code': 0b110, "name": "dh"},
	'bh': {'size': 8, 'code': 0b111, "name": "bh"},
	# 16-bits
	'ax': {'size': 16, 'code': 0b000, "name": "ax"},
	'cx': {'size': 16, 'code': 0b001, "name": "cx"},
	'dx': {'size': 16, 'code': 0b010, "name": "dx"},
	'bx': {'size': 16, 'code': 0b011, "name": "bx"},
	'sp': {'size': 16, 'code': 0b100, "name": "sp"},
	'bp': {'size': 16, 'code': 0b101, "name": "bp"},
	'si': {'size': 16, 'code': 0b110, "name": "si"},
	'di': {'size': 16, 'code': 0b111, "name": "di"},
	# 32-bits
	'eax': {'size': 32, 'code': 0b000, "name": "eax"},
	'ecx': {'size': 32, 'code': 0b001, "name": "ecx"},
	'edx': {'size': 32, 'code': 0b010, "name": "edx"},
	'ebx': {'size': 32, 'code': 0b011, "name": "ebx"},
	'esp': {'size': 32, 'code': 0b100, "name": "esp"},
	'ebp': {'size': 32, 'code': 0b101, "name": "ebp"},
	'esi': {'size': 32, 'code': 0b110, "name": "esi"},
	'edi': {'size': 32, 'code': 0b111, "name": "edi"},
	# 64-bits TODO
	'rax': {'size': 64, 'code': 0b000, "name": "rax"},
	'rcx': {'size': 64, 'code': 0b001, "name": "rcx"},
	'rdx': {'size': 64, 'code': 0b010, "name": "rdx"},
	'rbx': {'size': 64, 'code': 0b011, "name": "rbx"},
	'rsp': {'size': 64, 'code': 0b100, "name": "rsp"},
	'rbp': {'size': 64, 'code': 0b101, "name": "rbp"},
	'rsi': {'size': 64, 'code': 0b110, "name": "rsi"},
	'rdi': {'size': 64, 'code': 0b111, "name": "rdi"},
}

