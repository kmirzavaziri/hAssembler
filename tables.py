# Tables
# by Kamyar Mirzavaziri
# Contains Operator Codes and Register Codes

# ----------------------------------------------- TABLE OF OP-CODES -----------------------------------------------
# coderr is the OpCode for situations
#	op reg, reg | op reg, mem | op mem, reg
# codei is the OpCode for situations
#	op reg, imd | op mem, imd
# codea is the OpCode for situations
#	op  al, imd | op  ax, imd | op eax, imd | op rax, imd
operators = [
	# binary
	{"ops": 2, "coder": 0b000000, "codei": 0b100000000, "codea": 0b000001, "name": "add" },
	{"ops": 2, "coder": 0b000010, "codei": 0b100000001, "codea": 0b000011, "name": "or"  },
	{"ops": 2, "coder": 0b000100, "codei": 0b100000010, "codea": 0b000101, "name": "adc" },
	{"ops": 2, "coder": 0b000110, "codei": 0b100000011, "codea": 0b000111, "name": "sbb" },
	{"ops": 2, "coder": 0b001000, "codei": 0b100000100, "codea": 0b001001, "name": "and" },
	{"ops": 2, "coder": 0b001010, "codei": 0b100000101, "codea": 0b001011, "name": "sub" },
	{"ops": 2, "coder": 0b001100, "codei": 0b100000110, "codea": 0b001101, "name": "xor" },
	{"ops": 2, "coder": 0b001110, "codei": 0b100000111, "codea": 0b001111, "name": "cmp" },
	# unary
	{"ops": 1, "coder": 0b111111000, "name": "inc"},
	{"ops": 1, "coder": 0b111111001, "name": "dec"},
]

def tableOp(name):
	name = name.lower()
	for op in operators:
		if name.startswith(op['name']):
			if name[len(op['name']):] == '':
				return {**op, 'size': 0}
			if name[len(op['name']):] == 'b':
				return {**op, 'size': 8}
			elif name[len(op['name']):] == 'w':
				return {**op, 'size': 16}
			elif name[len(op['name']):] == 'd':
				return {**op, 'size': 32}
			elif name[len(op['name']):] == 'q':
				return {**op, 'size': 64}
	return {}

def tableOpByCode(code):
	for op in operators:
		if code == op['coder']:
			return op
		if code == op['codei'] >> 3:
			return op
		if code == op['codea']:
			return op
	return {}
def tableOpByCodeI(code):
	for op in operators:
		if code == op['codei']:
			return op
	return {}

# ---------------------------------------------- TABLE OF REGISTERS -----------------------------------------------
registers = [
	# 8-bits
	{'size': 8, 'code': 0b0000, "name": "al"  },
	{'size': 8, 'code': 0b0001, "name": "cl"  },
	{'size': 8, 'code': 0b0010, "name": "dl"  },
	{'size': 8, 'code': 0b0011, "name": "bl"  },
	{'size': 8, 'code': 0b0100, "name": "ah"  },
	{'size': 8, 'code': 0b0101, "name": "ch"  },
	{'size': 8, 'code': 0b0110, "name": "dh"  },
	{'size': 8, 'code': 0b0111, "name": "bh"  },
	{'size': 8, 'code': 0b1000, "name": "r8b" },
	{'size': 8, 'code': 0b1001, "name": "r9b" },
	{'size': 8, 'code': 0b1010, "name": "r10b"},
	{'size': 8, 'code': 0b1011, "name": "r11b"},
	{'size': 8, 'code': 0b1100, "name": "r12b"},
	{'size': 8, 'code': 0b1101, "name": "r13b"},
	{'size': 8, 'code': 0b1110, "name": "r14b"},
	{'size': 8, 'code': 0b1111, "name": "r15b"},
	# 16-bits
	{'size': 16, 'code': 0b0000, "name": "ax"  },
	{'size': 16, 'code': 0b0001, "name": "cx"  },
	{'size': 16, 'code': 0b0010, "name": "dx"  },
	{'size': 16, 'code': 0b0011, "name": "bx"  },
	{'size': 16, 'code': 0b0100, "name": "sp"  },
	{'size': 16, 'code': 0b0101, "name": "bp"  },
	{'size': 16, 'code': 0b0110, "name": "si"  },
	{'size': 16, 'code': 0b0111, "name": "di"  },
	{'size': 16, 'code': 0b1000, "name": "r8w" },
	{'size': 16, 'code': 0b1001, "name": "r9w" },
	{'size': 16, 'code': 0b1010, "name": "r10w"},
	{'size': 16, 'code': 0b1011, "name": "r11w"},
	{'size': 16, 'code': 0b1100, "name": "r12w"},
	{'size': 16, 'code': 0b1101, "name": "r13w"},
	{'size': 16, 'code': 0b1110, "name": "r14w"},
	{'size': 16, 'code': 0b1111, "name": "r15w"},
	# 32-bits
	{'size': 32, 'code': 0b0000, "name": "eax" },
	{'size': 32, 'code': 0b0001, "name": "ecx" },
	{'size': 32, 'code': 0b0010, "name": "edx" },
	{'size': 32, 'code': 0b0011, "name": "ebx" },
	{'size': 32, 'code': 0b0100, "name": "esp" },
	{'size': 32, 'code': 0b0101, "name": "ebp" },
	{'size': 32, 'code': 0b0110, "name": "esi" },
	{'size': 32, 'code': 0b0111, "name": "edi" },
	{'size': 32, 'code': 0b1000, "name": "r8d" },
	{'size': 32, 'code': 0b1001, "name": "r9d" },
	{'size': 32, 'code': 0b1010, "name": "r10d"},
	{'size': 32, 'code': 0b1011, "name": "r11d"},
	{'size': 32, 'code': 0b1100, "name": "r12d"},
	{'size': 32, 'code': 0b1101, "name": "r13d"},
	{'size': 32, 'code': 0b1110, "name": "r14d"},
	{'size': 32, 'code': 0b1111, "name": "r15d"},
	# 64-bits
	{'size': 64, 'code': 0b0000, "name": "rax"},
	{'size': 64, 'code': 0b0001, "name": "rcx"},
	{'size': 64, 'code': 0b0010, "name": "rdx"},
	{'size': 64, 'code': 0b0011, "name": "rbx"},
	{'size': 64, 'code': 0b0100, "name": "rsp"},
	{'size': 64, 'code': 0b0101, "name": "rbp"},
	{'size': 64, 'code': 0b0110, "name": "rsi"},
	{'size': 64, 'code': 0b0111, "name": "rdi"},
	{'size': 64, 'code': 0b1000, "name": "r8" },
	{'size': 64, 'code': 0b1001, "name": "r9" },
	{'size': 64, 'code': 0b1010, "name": "r10"},
	{'size': 64, 'code': 0b1011, "name": "r11"},
	{'size': 64, 'code': 0b1100, "name": "r12"},
	{'size': 64, 'code': 0b1101, "name": "r13"},
	{'size': 64, 'code': 0b1110, "name": "r14"},
	{'size': 64, 'code': 0b1111, "name": "r15"},
]

def tableReg(name):
	name = name.lower()
	for reg in registers:
		if name == reg['name']:
			return reg
	return {}

def tableRegByCodeSize(code, size):
	for reg in registers:
		if code == reg['code'] and size == reg['size']:
			return reg
	return {}

