opCodes = { #TODO
	"add": {"ops": 2, "coderr": 0b000000},
	"mov": {"ops": 2, "coderr": 0b100010, "coderi": 0b1011},
}

registers = {
	# 8-bits
	'al': {'size': 8, 'code': 0b000},
	'cl': {'size': 8, 'code': 0b001},
	'dl': {'size': 8, 'code': 0b010},
	'bl': {'size': 8, 'code': 0b011},
	'ah': {'size': 8, 'code': 0b100},
	'ch': {'size': 8, 'code': 0b101},
	'dh': {'size': 8, 'code': 0b110},
	'bh': {'size': 8, 'code': 0b111},
	# 16-bits
	'ax': {'size': 16, 'code': 0b000},
	'cx': {'size': 16, 'code': 0b001},
	'dx': {'size': 16, 'code': 0b010},
	'bx': {'size': 16, 'code': 0b011},
	'sp': {'size': 16, 'code': 0b100},
	'bp': {'size': 16, 'code': 0b101},
	'si': {'size': 16, 'code': 0b110},
	'di': {'size': 16, 'code': 0b111},
	# 32-bits
	'eax': {'size': 32, 'code': 0b000},
	'ecx': {'size': 32, 'code': 0b001},
	'edx': {'size': 32, 'code': 0b010},
	'ebx': {'size': 32, 'code': 0b011},
	'esp': {'size': 32, 'code': 0b100},
	'ebp': {'size': 32, 'code': 0b101},
	'esi': {'size': 32, 'code': 0b110},
	'edi': {'size': 32, 'code': 0b111}
	# 64-bits TODO
}

