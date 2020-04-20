# Instruction Class
# by Kamyar Mirzavaziri
# Contains a class called Instruction which stores all datas of a single instruction and can return it in both assembly and machine language

from tables import *
from eval import evaluate

################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
#------------------------------------------------ HELPER FUNCS ------------------------------------------------#
################################################################################################################
def bitsLen(num):
	if -2**7 <= num < 2**7:
		return 8
	elif -2**31 <= num < 2**31:
		return 32
	elif -2**63 <= num < 2**63:
		return 64
	else:
		return -1
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
		if tableReg(op) != {}:
			return {'type': 'reg', 'data': tableReg(op)}
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
				if tableReg(exp) != {}:
					# treating as base
					if base == {}:
						base = tableReg(exp)
					# treating as index
					elif index == {}:
							index = tableReg(exp)
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
							if tableReg(innerExp) != {}:
								if tmpIndex == {}:
									tmpIndex = tableReg(innerExp)
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
				raise Exception("invalid base/index expression: '" + index['name'] + "' cannot be index")
			
		return {'type': 'mem', 'data': {'base': base, 'index': index, 'scale': scale, 'disp': disp}}

################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
#---------------------------------------------- INSTRUCTION CLASS ---------------------------------------------#
################################################################################################################
class Instruction:
	def __init__(self):
	########################################################################
	#------------------------- Assembly Code Data -------------------------#
	########################################################################
		self.operator = {}
		self.operands = []

	########################################################################
	#------------------------- Machine Code Data --------------------------#
	########################################################################
		# Prefix: 0-4 B
		self.prefix = []
		# REX: 0-1 B ?= 2 b + 3 b + 3 b
		# (if [rex] then we have REX byte, else we don't)
		self.rex = False
		self.rexW = 0b0
		self.rexR = 0b0
		self.rexX = 0b0
		self.rexB = 0b0
		# OpCode: 1 B = 6 b + 1 b + 1 b
		self.mainOpCode = 0b000000
		self.direction = 0b0
		self.w = 0b0
		# AddrMode: 0-1 B ?= 2 b + 3 b + 3 b
		# (if [addrMode] then we have AddrMode byte, else we don't)
		self.addrMode = True
		self.mod = 0b00
		self.reg = 0b000
		self.rm = 0b000
		# SIB: 0-1 B ?= 2 b + 3 b + 3 b
		# (if [sib] then we have SIB byte, else we don't)
		self.sib = False
		self.scale = 0b00
		self.index = 0b000
		self.base = 0b000
		# Displacement: 0-4 B
		self.disp = []
		# Data: 0-8 B
		self.data = []

	########################################################################
	#--------------------------- TO-STRING FUNC ---------------------------#
	########################################################################
	def toString(self):
		colW = 30
		return ' '.join(map("{0:02X}".format, self.machineCode)).ljust(colW) + '\t' + self.assemblyCode

	########################################################################
	#------------------------------ BINTOOBJ ------------------------------#
	########################################################################
	def fromBin(self, stream):
		dataSize = 0
		dispSize = 0
		# read prefixes
		while stream != [] and (stream[0] >> 4) == 0b0110:
			self.prefix += [stream[0]]
			stream = stream[1:]

		if len(self.prefix) > 4:
			raise Exception("more than 4 bytes prefix")

		# read possible REX
		rex = []
		while stream != [] and stream[0] >> 4 == 0b0100:
			rex += [stream[0]]
			stream = stream[1:]

		if len(rex) > 1:
			raise Exception("more than 1 byte REX")

		if rex != []:
			self.rex = True
			self.rexW = (rex[0] >> 3) & 0b1
			self.rexR = (rex[0] >> 2) & 0b1
			self.rexX = (rex[0] >> 1) & 0b1
			self.rexB = (rex[0] >> 0) & 0b1

		# read opCode
		if stream == []:
			raise Exception("OpCode not found")
		
		opCode = stream[0]
		stream = stream[1:]
		
		self.mainOpCode = opCode >> 2
		self.direction = (opCode >> 1) & 0b1
		self.w = (opCode >> 0) & 0b1

		self.operator = tableOpByCode(self.mainOpCode)
		if self.operator == {}:
			raise Exception("unknow OpCode")

		# proccess opCode - may figure out the operation
		opType = 'r'
		if self.operator['codea'] == self.mainOpCode:
			opType = 'a'
			self.addrMode = False
			size = self.getRegSize()
			self.operands = [{}]
			self.operands[0] = operand(tableRegisterByCodeSize(0b0000, size)['name'])
			dataSize = 1 # TODO

		# read possible AddrMode
		if self.addrMode:
			if stream == []:
				raise Exception("AddrMode not found")
			addrMode = stream[0]
			stream = stream[1:]
			
			self.mod = addrMode >> 6
			self.reg = (addrMode >> 3) & 0b111
			self.rm  = (addrMode >> 0) & 0b111

			# figure out the operation (or already figured out)
			if self.operator['ops'] == 1 or self.operator['codei'] >> 3 == self.mainOpCode:
				opType = 'i'
				self.operator = tableOpByCodeI(self.mainOpCode << 3 | self.reg)
				if self.operator == {}:
					raise Exception("unknow OpCode")
				
			# mod case analysis
			if self.mod == 0b11:
				self.operands = [{}]
				self.operands[0] = operand(self.getRegRm()['name'])
				self.sib = False
				if self.operator['ops'] > 1:
					if opType == 'r':
						self.operands += [{}]
						self.operands[1] = operand(self.getRegReg()['name'])
					elif opType == 'i':
						opType = 'i' # TODO
		# read possible SIB
		if self.sib:
			if stream == []:
				raise Exception("SIB not found")
			sib = stream[0]
			stream = stream[1:]
			
			self.scale = sib >> 6
			self.index = (sib >> 3) & 0b111
			self.base  = (sib >> 0) & 0b111

		# read possible disp
		if len(stream) < dispSize:
			raise Exception("displacement not found")
		self.disp = stream[0:dispSize]
		stream = stream[dispSize:]

		# read possible data
		if len(stream) < dataSize:
			raise Exception("data not found")
		self.data = stream[0:dataSize]
		stream = stream[dataSize:]
		
		return stream


	# ---------------------------- END BINTOOBJ ----------------------------

	########################################################################
	#------------------------------ ASMTOOBJ ------------------------------#
	########################################################################
	def fromAsm(self, head, tail):
		# ---------------- Primary Proccessing ----------------
		# proccess head
		self.operator = tableOp(head)
		if self.operator == {}:
			raise Exception("no such operation: '" + head + "'")

		# proccess head tail
		self.operands = tail.split(',')
		if self.operands == ['']:
			self.operands = []
		self.operands = list(map(operand, self.operands))

		# head and tail mismatch
		if len(self.operands) != self.operator["ops"]:
			raise Exception("number of operands mismatch for '" + head + "'")

		# --------------- Secondary Proccessing ---------------
		# Unary Operator
		if self.operator["ops"] == 1:
			# --------------- reg ---------------
			if self.operands[0]['type'] == 'reg':
				# operation size
				if self.operator['size'] != 0 and self.operator['size'] != self.operands[0]['data']['size']:
					raise Exception("suffix and operand type mistmach for '" + head + "'")
				# opCode
				self.mainOpCode = self.operator['coder'] >> 3
				self.reg = self.operator['coder'] & 0b111
				# direction
				self.direction = 0b1
				# op 0
				self.setRegRm(self.operands[0]['data'])
			# --------------- mem ---------------
			elif self.operands[0]['type'] == 'mem':
				# operation size
				if self.operator['size'] == 0:
					raise Exception("ambiguous operand size for '" + head + "'")
				else:
					self.setRegSize(self.operator['size'])
				# opCode
				self.mainOpCode = self.operator['coder'] >> 3
				self.reg = self.operator['coder'] & 0b111
				# direction
				self.direction = 0b1
				# op 0
				self.setMem(self.operands[0]['data'])
			# --------------- imd ---------------
			elif self.operands[0]['type'] == 'imd':
				raise Exception("operand type mismatch for '" + head + "'")
		# Binary Operator
		elif self.operator["ops"] == 2:
			# --------------- reg, reg ---------------
			if self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'reg':
				# operation size
				if self.operands[0]['data']['size'] != self.operands[1]['data']['size']:
					raise Exception("operand type mismatch for '" + head + "'")
				if self.operator['size'] != 0 and self.operator['size'] != self.operands[0]['data']['size']:
					raise Exception("suffix and operand type mistmach for '" + head + "'")
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
				# operation size
				if self.operator['size'] != 0 and self.operator['size'] != self.operands[0]['data']['size']:
					raise Exception("suffix and operand type mistmach for '" + head + "'")
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
				# operation size
				if self.operator['size'] != 0 and self.operator['size'] != self.operands[0]['data']['size']:
					raise Exception("suffix and operand type mistmach for '" + head + "'")
				size = min(self.operands[0]['data']['size'], bitsLen(self.operands[1]['data']))
				# opCode
				self.mainOpCode = self.operator['codei'] >> 3
				self.reg = self.operator['codei'] & 0b111
				# direction (sign-extended here)
				if bitsLen(self.operands[1]['data']) == 8 and self.operands[0]['data']['size'] > 8:
					self.direction = 0b1
				else:
					self.direction = 0b0
				# op 0
				self.setRegRm(self.operands[0]['data'])
				# op 1
				self.setImdData(self.operands[1]['data'], size)
				# special case for al, ax, eax, rax (code = 0b0000)
				if self.operands[0]['data']['code'] == 0b0000:
					self.addrMode = False
					self.mainOpCode = self.operator['codea']
			# --------------- mem, reg ---------------
			elif self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'reg':
				# operation size
				if self.operator['size'] != 0 and self.operator['size'] != self.operands[1]['data']['size']:
					raise Exception("suffix and operand type mistmach for '" + head + "'")
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
				# operation size
				if self.operator['size'] == 0:
					raise Exception("ambiguous operand size for '" + head + "'")
				else:
					size = self.operator['size']
				# opCode
				self.mainOpCode = self.operator['codei'] >> 3
				self.reg = self.operator['codei'] & 0b111
				# direction (sign-extended here)
				if bitsLen(self.operands[1]['data']) == 8 and size > 8:
					self.direction = 0b1
				else:
					self.direction = 0b0
				# op 0
				self.setMem(self.operands[0]['data'])
				# op 1
				self.setImdData(self.operands[1]['data'], min(bitsLen(self.operands[1]['data']), size))
				self.setRegSize(size)
			# --------------- imd, reg ---------------
			# --------------- imd, mem ---------------
			# --------------- imd, imd ---------------
			elif self.operands[0]['type'] == 'imd':
				raise Exception("operand type mismatch for '" + head + "'")
	# ---------------------------- END ASMTOOBJ ----------------------------

	########################################################################
	#---------------------------- HELPER FUNCS ----------------------------#
	########################################################################
	def setRegReg(self, register):
		self.reg = register['code']
		self.setRegSize(register['size'])

	def getRegReg(self):
		code = self.rexR << 3 | self.reg
		size = self.getRegSize()
		reg = tableRegByCodeSize(code, size)
		if reg == {}:
			raise Exception("unknown register with code '" + code + "' and size " + size)
		return reg

	def setRegRm(self, register):
		self.mod = 0b11
		self.rm = register['code']
		self.setRegSize(register['size'])

	def getRegRm(self):
		code = self.rexB << 3 | self.rm
		size = self.getRegSize()
		reg = tableRegByCodeSize(code, size)
		if reg == {}:
			raise Exception("unknown register with code '" + code + "' and size " + size)
		return reg
		
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

	def getRegSize(self, isAddress = False):
		if not isAddress:
			if self.rexW == 0b0 and self.w == 0b0 and not 0x66 in self.prefix:
				return 8
			elif self.rexW == 0b0 and self.w == 0b1 and 0x66 in self.prefix:
				return 16
			elif self.rexW == 0b0 and self.w == 0b1 and not 0x66 in self.prefix:
				return 32
			elif self.rexW == 0b1 and self.w == 0b1 and not 0x66 in self.prefix:
				return 64
			else:
				raise Exception("inconsistent code")
				
		else:
			if 0x67 in self.prefix:
				return 32
			else:
				return 64

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
		fake = False
		base = val['base']
		index = val['index']
		scale = val['scale']
		disp = val['disp']
		
		# taking care of displacement
		if disp == 0 and (base == {} or base['code'] & 0b111 != 0b101):
			self.mod = 0b00
		elif bitsLen(disp) == 8:
			self.mod = 0b01
			self.setDisp(disp, 8)
		elif bitsLen(disp) == 32:
			self.mod = 0b10
			self.setDisp(disp, 32)
		else:
			raise Exception(hex(disp) + " displacement overflow")

		# esp special case
		if index == {} and base != {} and base['code'] & 0b111 == 0b100:
			fake = True
			index = base.copy()
			index['code'] &= 0b111
			self.rm = base['code']
			self.setRegSize(base['size'], True)

		# ebp special case
		if  index != {} and base != {} and base['code'] & 0b111 == 0b101:
			fake = True
			self.setRegSize(base['size'], True)

		# scaled addressing [scale*index]
		if index != {} and base == {}:
			fake = True
			self.mod = 0b00
			base = tableReg('ebp')
			self.setDisp(disp, 32)
			self.setRegSize(index['size'], True)
		# direct addressing [disp]
		elif index == {} and base == {}:
			fake = True
			self.mod = 0b00
			base = tableReg('ebp')
			index = tableReg('esp')
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
			if not fake:
				self.setRegSize(base['size'], True)

	########################################################################
	#---------------------------- ASSEMBLY CODE ---------------------------#
	########################################################################
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
		
	########################################################################
	#---------------------------- MACHINE CODE ----------------------------#
	########################################################################
	@property
	def machineCode(self):
		# REX: B from rm
		if self.rm & 0b1000 == 0b1000:
			self.rex = True
			self.rexB = 0b1
			self.rm &= 0b111

		# REX: R from reg
		if self.reg & 0b1000 == 0b1000:
			self.rex = True
			self.rexR = 0b1
			self.reg &= 0b111

		# REX: B from base
		if self.base & 0b1000 == 0b1000:
			self.rex = True
			self.rexB = 0b1
			self.base &= 0b111

		# REX: X from index
		if self.index & 0b1000 == 0b1000:
			self.rex = True
			self.rexX = 0b1
			self.index &= 0b111

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
