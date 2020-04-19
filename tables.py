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
	'al': {'size': 8, 'code': 0b0000, "name": "al"},
	'cl': {'size': 8, 'code': 0b0001, "name": "cl"},
	'dl': {'size': 8, 'code': 0b0010, "name": "dl"},
	'bl': {'size': 8, 'code': 0b0011, "name": "bl"},
	'ah': {'size': 8, 'code': 0b0100, "name": "ah"},
	'ch': {'size': 8, 'code': 0b0101, "name": "ch"},
	'dh': {'size': 8, 'code': 0b0110, "name": "dh"},
	'bh': {'size': 8, 'code': 0b0111, "name": "bh"},
	# 16-bits
	'ax'  : {'size': 16, 'code': 0b0000, "name": "ax"  },
	'cx'  : {'size': 16, 'code': 0b0001, "name": "cx"  },
	'dx'  : {'size': 16, 'code': 0b0010, "name": "dx"  },
	'bx'  : {'size': 16, 'code': 0b0011, "name": "bx"  },
	'sp'  : {'size': 16, 'code': 0b0100, "name": "sp"  },
	'bp'  : {'size': 16, 'code': 0b0101, "name": "bp"  },
	'si'  : {'size': 16, 'code': 0b0110, "name": "si"  },
	'di'  : {'size': 16, 'code': 0b0111, "name": "di"  },
	'r8w' : {'size': 16, 'code': 0b1000, "name": "r8w" },
	'r9w' : {'size': 16, 'code': 0b1001, "name": "r9w" },
	'r10w': {'size': 16, 'code': 0b1010, "name": "r10w"},
	'r11w': {'size': 16, 'code': 0b1011, "name": "r11w"},
	'r12w': {'size': 16, 'code': 0b1100, "name": "r12w"},
	'r13w': {'size': 16, 'code': 0b1101, "name": "r13w"},
	'r14w': {'size': 16, 'code': 0b1110, "name": "r14w"},
	'r15w': {'size': 16, 'code': 0b1111, "name": "r15w"},
	# 32-bits
	'eax' : {'size': 32, 'code': 0b0000, "name": "eax" },
	'ecx' : {'size': 32, 'code': 0b0001, "name": "ecx" },
	'edx' : {'size': 32, 'code': 0b0010, "name": "edx" },
	'ebx' : {'size': 32, 'code': 0b0011, "name": "ebx" },
	'esp' : {'size': 32, 'code': 0b0100, "name": "esp" },
	'ebp' : {'size': 32, 'code': 0b0101, "name": "ebp" },
	'esi' : {'size': 32, 'code': 0b0110, "name": "esi" },
	'edi' : {'size': 32, 'code': 0b0111, "name": "edi" },
	'r8d' : {'size': 32, 'code': 0b1000, "name": "r8d" },
	'r9d' : {'size': 32, 'code': 0b1001, "name": "r9d" },
	'r10d': {'size': 32, 'code': 0b1010, "name": "r10d"},
	'r11d': {'size': 32, 'code': 0b1011, "name": "r11d"},
	'r12d': {'size': 32, 'code': 0b1100, "name": "r12d"},
	'r13d': {'size': 32, 'code': 0b1101, "name": "r13d"},
	'r14d': {'size': 32, 'code': 0b1110, "name": "r14d"},
	'r15d': {'size': 32, 'code': 0b1111, "name": "r15d"},
	# 64-bits
	'rax': {'size': 64, 'code': 0b0000, "name": "rax"},
	'rcx': {'size': 64, 'code': 0b0001, "name": "rcx"},
	'rdx': {'size': 64, 'code': 0b0010, "name": "rdx"},
	'rbx': {'size': 64, 'code': 0b0011, "name": "rbx"},
	'rsp': {'size': 64, 'code': 0b0100, "name": "rsp"},
	'rbp': {'size': 64, 'code': 0b0101, "name": "rbp"},
	'rsi': {'size': 64, 'code': 0b0110, "name": "rsi"},
	'rdi': {'size': 64, 'code': 0b0111, "name": "rdi"},
	'r8' : {'size': 64, 'code': 0b1000, "name": "r8" },
	'r9' : {'size': 64, 'code': 0b1001, "name": "r9" },
	'r10': {'size': 64, 'code': 0b1010, "name": "r10"},
	'r11': {'size': 64, 'code': 0b1011, "name": "r11"},
	'r12': {'size': 64, 'code': 0b1100, "name": "r12"},
	'r13': {'size': 64, 'code': 0b1101, "name": "r13"},
	'r14': {'size': 64, 'code': 0b1110, "name": "r14"},
	'r15': {'size': 64, 'code': 0b1111, "name": "r15"},
}

