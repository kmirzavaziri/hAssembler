# Instruction Class
# by Kamyar Mirzavaziri
# Contains a class called Instruction which stores all datas of a single instruction and can return it in both assembly and machine language

from tables import *
from eval import evaluate

# ------------------------------------------------ HELPER FUNCS ------------------------------------------------
def operand(op):
	# Check if memory addressing
	op = op.strip()
	isMemory = False
	if len(op) > 1 and op[0] == '[' and op[-1] == ']':
		isMemory = True
		op = op[1:-1]

	# Further Proccess
	if not isMemory:
		# register
		if op in registers:
			return {'type': 'reg', 'data': registers[op]}
		# immediate data
		try:
			return {'type': 'imd', 'data': evaluate(op)}
		except:
			raise Exception("invalid operand: '" + op + "'")
	# memory
	else:
		splittedOp = op.split('+')
		base = {}
		index = {}
		scale = 1
		disp = 0
		for exp in splittedOp:
			exp = exp.strip()
			# this exp is a constant
			try:
				disp += evaluate(exp)
			# this exp is not a constant
			except:
				# this exp is a register name
				if exp in registers:
					# treating as base
					if base == {}:
						base = registers[exp]
					# treating as index
					elif index == {}:
							index = registers[exp]
							scale = 1
					# both are currently occupied
					else:
						raise Exception("invalid base/index expression: too many registers")
				# this exp is a not a register name (should be index*scale)
				# Note: here we check if scale is 1, base is free and index is 
				# occupied, this should be valid if we put this 1-scaled index to base
				else:
					# evaluating this expression
					exp = exp.split('*')
					tmpScale = 1
					tmpIndex = {}
					for innerExp in exp:
						innerExp = innerExp.strip()
						# this innerExp is a constant
						try:
							tmpScale *= evaluate(innerExp)
						# this innerExp is not a constant (should be index which shouldn't be occupied)
						except:
							if innerExp in registers:
								if tmpIndex == {}:
									tmpIndex = registers[innerExp]
								else:
									raise Exception("invalid base/index expression: too many registers")
							# this innerExp can't be anything other than constant or register
							else:
								raise Exception("invalid base/index expression: unknown expression '" + innerExp + "'")
					# if scale is 1 and base is not currently occupied we prefer to put this 1-scaled index to base
					if tmpScale == 1 and base == {}:
						base = tmpIndex
					# else we should put it in index
					else:
						if index != {}:
							raise Exception("invalid base/index expression: too many registers")
						else:
							index = tmpIndex					
							scale = tmpScale
					# excluding invalid scales
					if not scale in [1,2,4,8]:
						raise Exception("invalid base/index expression: invalid scale '" + scale + "'")
		# catching some errors
		if base != {} and base['size'] < 32:
			raise Exception("invalid base/index expression: base should be 32-bit or 64-bit register")
		if base != {} and index != {} and base['size'] != index['size']:
			raise Exception("invalid base/index expression: base and index type mismatch")
		if index != {} and index['code'] == 0b100:
			if scale == 1:
				tmp = base
				base = index
				index = tmp
			else:
				raise Exception("invalid base/index expression: 'esp' cannot be index")
			
		return {'type': 'mem', 'data': {'base': base, 'index': index, 'scale': scale, 'disp': disp}}

# ---------------------------------------------- INSTRUCTION CLASS ---------------------------------------------
class Instruction:
	# ------------------------- Assembly Code Data -------------------------
	operator = {}
	operands = []
	# ------------------------- Machine Code Data --------------------------
	# Prefix: 0-4 B
	prefix = []
	# REX: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [rex] then we have REX byte, else we don't)
	rex = False
	rexW = 0b0
	rexR = 0b0
	rexX = 0b0
	rexB = 0b0
	# OpCode: 1 B = 6 b + 1 b + 1 b
	# Note: if not [moveAlter] then OpCode (1 B) = mainOpCode (4 b) + W (1 b) + reg (3 b)
	moveAlter = False
	mainOpCode = 0b000000
	direction = 0b0
	w = 0b0
	# AddrMode: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [addrMode] then we have AddrMode byte, else we don't)
	addrMode = True
	mod = 0b00
	reg = 0b000
	rm = 0b000
	# SIB: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [sib] then we have SIB byte, else we don't)
	sib = False
	scale = 0b00
	index = 0b000
	base = 0b000
	# Displacement: 0-4 B
	disp = []
	# Data: 0-8 B
	data = []

	# --------------------------- TO-STRING FUNC ---------------------------
	def toString(self):
		colW = 30
		return ' '.join(map("{0:02X}".format, self.machineCode)).ljust(colW) + '\t' + self.assemblyCode

	# ------------------------------ ASMTOOBJ ------------------------------
	def fromAsm(self, head, tail):
		# ---------------- Primary Proccessing ----------------
		raw = head + tail
		
		# Unknown Operation
		if not head in opCodes:
			raise Exception("no such instruction: '" + raw + "'")

		# Proccess head and tail
		self.operator = opCodes[head]
		self.operands = tail.split(',')
		if self.operands == ['']:
			self.operands = []
		self.operands = list(map(operand, self.operands))

		# Number mismatch
		if len(self.operands) != self.operator["ops"]:
			raise Exception("number of operands mismatch for '" + head + "'")

		# --------------- Secondary Proccessing ---------------
		# Unary Operator
		if self.operator["ops"] == 1:
			self.operator["ops"] = 1 # TODO
		# Binary Operator
		elif self.operator["ops"] == 2:
			##########################################
			# -------- handling special cases --------
			if(self.operator['name'] == 'test' and self.operands[1]['type'] == 'mem'):
				tmp = self.operands[0]
				self.operands[0] = self.operands[1]
				self.operands[1] = tmp

			##########################################
			# --------------- reg, reg ---------------
			if self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'reg':
				# same size condition
				if self.operands[0]['data']['size'] != self.operands[1]['data']['size']:
					raise Exception("operand type mismatch for '" + head + "'")
				# opCode
				self.mainOpCode = self.operator['coder']
				# direction
				self.direction = 0b0
				# op 0
				self.setRegRm(self.operands[0]['data'])
				# op 1
				self.setRegReg(self.operands[1]['data'])
				# may add two 0x66 prefixes
				if len(self.prefix) == 2:
					self.prefix = self.prefix[0:1]
			# --------------- reg, mem ---------------
			elif self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'mem':
				# opCode
				self.mainOpCode = self.operator['coder']
				# direction
				self.direction = 0b1
				# op 0
				self.setRegReg(self.operands[0]['data'])
				# op 1
				self.setMem(self.operands[1]['data'])
			# --------------- reg, imd ---------------
			elif self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'imd':
				# opCode
				# Note: mov operator has alternate encoding
				if(self.operator['name'] == 'mov'):
					self.addrMode = False
					self.moveAlter = True
					self.mainOpCode = self.operator['codei']
				else:
					self.mainOpCode = self.operator['codei'] >> 3
					self.reg = self.operator['codei'] & 0b111
				# direction (sign-extended here)
				self.direction = 0b0
				# op 0
				self.setRegRm(self.operands[0]['data'])
				# op 1
				self.setImdData(self.operands[1]['data'], self.operands[0]['data']['size'])
			# --------------- mem, reg ---------------
			elif self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'reg':
				# opCode
				self.mainOpCode = self.operator['coder']
				# direction
				self.direction = 0b0
				# op 0
				self.setMem(self.operands[0]['data'])
				# op 1
				self.setRegReg(self.operands[1]['data'])
			# --------------- mem, mem ---------------
			elif self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'mem':
				raise Exception("too many memory references for '" + head + "'")
			# --------------- mem, imd ---------------
			elif self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'imd':
				# opCode
				self.mainOpCode = self.operator['codei'] # TODO
				# addrMode
				self.addrMode = True # TODO
				# direction
				self.direction = 0b1
				# op 0
				# TODO mem
				# op 1
				# TODO imd
			# --------------- imd, reg ---------------
			# --------------- imd, mem ---------------
			# --------------- imd, imd ---------------
			elif self.operands[0]['type'] == 'imd':
				raise Exception("operand type mismatch for '" + head + "'")
	# ---------------------------- END ASMTOOBJ ----------------------------

	# ---------------------------- HELPER FUNCS ----------------------------
	def setRegReg(self, register):
		self.reg = register['code']
		self.setRegSize(register['size'])

	def setRegRm(self, register):
		self.mod = 0b11
		self.rm = register['code']
		self.setRegSize(register['size'])

	def setRegSize(self, size, isAddress = False):
		if not isAddress:
			if size == 8:
				self.w = 0b0
			elif size == 16:
				self.w = 0b1
				self.prefix = self.prefix + [0x66]
			elif size == 32:
				self.w = 0b1
			elif size == 64:
				self.rex = True
				self.w = 0b1
				self.rexW = 0b1
		else:
			if size == 32:
				self.prefix = [0x67] + self.prefix

	def setImdData(self, val, size):
		self.data = [0x00] * (size // 8)
		for i in range(len(self.data)):
			self.data[i] = val & 0xFF
			val >>= 8

	def setDisp(self, val, size):
		self.disp = [0x00] * (size // 8)
		for i in range(len(self.disp)):
			self.disp[i] = val & 0xFF
			val >>= 8

	def setMem(self, val):
		base = val['base']
		index = val['index']
		scale = val['scale']
		disp = val['disp']
		
		# taking care of displacement
		if disp == 0 and (base == {} or base['code'] != 0b101):
			self.mod = 0b00
		elif disp.bit_length() <= 7:
			self.mod = 0b01
			self.setDisp(disp, 8)
		elif disp.bit_length() <= 31:
			self.mod = 0b10
			self.setDisp(disp, 32)
		else:
			raise Exception(hex(disp) + " displacement overflow")

		# esp special case
		if index == {} and base != {} and base['code'] == 0b100:
			index = base
			self.rm = base['code']
			self.setRegSize(base['size'], True)

		# ebp special case
		if  index != {} and base != {} and base['code'] == 0b101:
			self.setRegSize(base['size'], True)

		# scaled addressing [scale*index]
		if index != {} and base == {}:
			self.mod = 0b00
			base = registers['ebp']
			self.setDisp(disp, 32)
			self.setRegSize(index['size'], True)
		# direct addressing [disp]
		elif index == {} and base == {}:
			self.mod = 0b00
			base = registers['ebp']
			index = registers['esp']
			scale = 1
			self.setDisp(disp, 32)


		# register addressing [base]
		if index == {} and base != {}:
			self.rm = base['code']
			self.setRegSize(base['size'], True)
		# complete addresing [base + scale * index + disp]
		elif index != {} and base != {}:
			self.rm = 0b100
			self.sib = True
			if scale == 1:
				self.scale = 0b00
			elif scale == 2:
				self.scale = 0b01
			elif scale == 4:
				self.scale = 0b10
			elif scale == 8:
				self.scale = 0b11
			self.index = index['code']
			self.base = base['code']
			if self.index != 0b100 and self.base != 0b101:
				self.setRegSize(base['size'], True)

	# ---------------------------- ASSEMBLY CODE ---------------------------
	@property
	def assemblyCode(self):
		operands = []
		for operand in self.operands:
			if operand['type'] == 'reg':
				operands.append(operand['data']['name'])
			elif operand['type'] == 'mem':
				base = operand['data']['base']
				index = operand['data']['index']
				scale = operand['data']['scale']
				disp = operand['data']['disp']
				if disp == 0:
					dispStr = ''
				else:
					dispStr = ' + ' + hex(disp)

				if base == {} and index == {}:
					operands.append('[' + hex(disp) + ']')
				elif base == {} and index != {}:
					operands.append('[' + index['name'] + '*' + hex(scale) + dispStr + ']')
				elif base != {} and index == {}:
					operands.append('[' + base['name'] + dispStr + ']')
				elif base != {} and index != {}:
					operands.append('[' + base['name'] + ' + ' + index['name'] + '*' + hex(scale) + dispStr + ']')
			elif operand['type'] == 'imd':
				operands.append(hex(operand['data']))
		return self.operator['name'] + ' ' + ', '.join(operands)
		
	# ---------------------------- MACHINE CODE ----------------------------
	@property
	def machineCode(self):
		rex = []
		if self.rex:
			rex = [ 0b0100 << 4 | (self.rexW << 3) | (self.rexR << 2) | (self.rexX << 1) | (self.rexB) ]
		else:
			rex = []

		sib = []
		if self.sib:
			sib = [ (self.scale << 6) | (self.index << 3) | (self.base) ]
		else:
			sib = []

		opCode = []
		if self.moveAlter:
			opCode = [ (self.mainOpCode << 4) | (self.w << 3) | (self.rm) ]
		else:
			opCode = [ (self.mainOpCode << 2) | (self.direction << 1) | (self.w) ]

		addrMode = []
		if self.addrMode:
			addrMode = [ (self.mod << 6) | (self.reg << 3) | (self.rm) ]
		else:
			addrMode = []
		return \
			self.prefix + \
			rex + \
			opCode + \
			addrMode + \
			sib + \
			self.disp + \
			self.data
# -------------------------------------------- END INSTRUCTION CLASS -------------------------------------------
# EOF
