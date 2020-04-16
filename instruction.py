opCodes = { #TODO
	"add": {"code": 0b000000, "ops": 2},
	"mov": {"code": 0b100010, "ops": 2}
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
}

def operand(op):
	# Check if memory addressing
	op = op.strip()
	mem = False
	if len(op) > 1 and op[0] == '[' and op[-1] == ']':
		mem = True
		op = op[1:-1]

	# Further Proccess
	if not mem:
		if op in registers:
			return {'type': 'reg', 'data': registers[op]}
		return {'type': 'imd', 'data': eval(op)} # TODO eval

	# TODO immidiate, indirect, scale, indirect with scale, ...
		
# 64-bits TODO

class Instruction:
	# Prefix: 0-4 B
	prefix = []
	# Rex: 0-1 B
	rex = []
	# OpCode: 1 B = 6 b + 1 b + 1 b
	mainOpCode = 0b000000
	direction = 0b0
	operandLength = 0b0
	# AddrMode: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [addrMode] is 1 then we have AddrMode byte, else we don't)
	addrMode = 0b0
	mod = 0b00
	reg = 0b000
	rm = 0b000
	# SIB: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [sib] is 1 then we have SIB byte, else we don't)
	sib = 0b0
	scale = 0b00
	index = 0b000
	base = 0b000
	# Displacement: 0-4 B
	displacement = []
	# Data: 0-8 B
	data = []
	# -------------------------------- INIT --------------------------------
	def __init__ (self, head, tail):
		# ---------------- Primary Proccessing ----------------
		raw = head + tail
		
		# Unknown Operation
		if not head in opCodes:
			raise Exception("no such instruction: '" + raw + "'")

		# Proccess head and tail
		operator = opCodes[head]
		operands = list(map(operand, tail.split(',')))
		self.mainOpCode = operator['code']
		
		# Number mismatch
		if len(operands) != operator["ops"]:
			raise Exception("number of operands mismatch for '" + head + "'")

		# --------------- Secondary Proccessing ---------------
		# Unary Operator
		if operator["ops"] == 1:
			operator["ops"] = 1 # TODO
		# Binary Operator
		elif operator["ops"] == 2:
			# --------------- reg, reg ---------------
			if operands[0]['type'] == 'reg' and operands[1]['type'] == 'reg':
				# same size condition
				if operands[0]['data']['size'] != operands[1]['data']['size']:
					raise Exception("operand type mismatch for '" + head + "'")
				# direction
				self.direction = 0b0
				# op 0
				self.setRegRm(operands[0]['data'])
				# op 1
				self.mod = 0b11
				self.setRegReg(operands[1]['data'])
			# --------------- reg, mem ---------------
			if operands[0]['type'] == 'reg' and operands[1]['type'] == 'mem':
				# direction
				self.direction = 0b1
				# op 0
				self.setRegReg(operands[0]['data'])
				# op 1
				# TODO mem
			# --------------- reg, imd ---------------
			if operands[0]['type'] == 'reg' and operands[1]['type'] == 'imd':
				# direction
				self.direction = 0b1
				# op 0
				self.setRegReg(operands[0]['data'])
				# op 1
				# TODO imd
			# --------------- mem, reg ---------------
			if operands[0]['type'] == 'mem' and operands[1]['type'] == 'reg':
				# direction
				self.direction = 0b0
				# op 0
				# TODO mem
				# op 1
				self.setRegReg(operands[1]['data'])
			# --------------- mem, mem ---------------
			if operands[0]['type'] == 'mem' and operands[1]['type'] == 'mem':
				raise Exception("too many memory references for '" + head + "'")
			# --------------- mem, imd ---------------
			if operands[0]['type'] == 'mem' and operands[1]['type'] == 'imd':
				# direction
				self.direction = 0b1
				# op 0
				# TODO mem
				# op 1
				# TODO imd
			# --------------- imd, reg ---------------
			# --------------- imd, mem ---------------
			# --------------- imd, imd ---------------
			if operands[0]['type'] == 'imd':
				raise Exception("operand type mismatch for '" + head + "'")
	# ------------------------------ INIT-END ------------------------------

	def setRegReg(self, register):
		self.reg = register['code']
		self.setRegSize(register['size'])

	def setRegRm(self, register):
		self.rm = register['code']
		self.setRegSize(register['size'])

	def setRegSize(self, size):
		if size == 8:
			self.w = 0b0
			self.prefix = []
		elif size == 16:
			self.w = 0b1
			self.prefix = [0x66]
		elif size == 32:
			self.w = 0b1
			self.prefix = []

	def toMachineCode(self):
		sib = []
		if self.sib:
			sib = [ (self.scale << 6) | (self.index << 3) | (self.base) ]
		return \
			self.prefix + \
			self.rex + \
			[ (self.mainOpCode << 2) | (self.direction << 1) | (self.operandLength) ] + \
			[ (self.mod << 6) | (self.reg << 3) | (self.rm) ] + \
			sib + \
			self.displacement + \
			self.data
			
