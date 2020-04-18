# This file contains a class called Instruction which stores all datas of
# a single instruction and can print it in both assembly and machine language

import ast

from tables import *

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
			return {'type': 'reg', 'data': {**registers[op] , 'name': op}}
		# immediate data
		try:
			return {'type': 'imd', 'data': ast.literal_eval(op)}
		except:
			raise Exception("unable to evalute immediate data expression")

	# TODO indirect, scale, indirect with scale, ...	

class Instruction:
	# ------------------------- Assembly Code Data -------------------------
	# ------------------------- Machine Code Data --------------------------
	# Prefix: 0-4 B
	prefix = []
	# Rex: 0-1 B
	rex = []
	# OpCode: 1 B = 6 b + 1 b + 1 b
	# Note: if not [addrMode] then OpCode (1 B) = mainOpCode (4 b) + W (1 b) + reg (3 b)
	mainOpCode = 0b000000
	direction = 0b0
	w = 0b0
	# AddrMode: 0-1 B ?= 2 b + 3 b + 3 b
	# (if [addrMode] then we have AddrMode byte, else we don't)
	addrMode = False
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
		self.operator = {**opCodes[head], 'name': head}
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
			# --------------- reg, reg ---------------
			if self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'reg':
				# same size condition
				if self.operands[0]['data']['size'] != self.operands[1]['data']['size']:
					raise Exception("operand type mismatch for '" + head + "'")
				# opCode
				self.mainOpCode = operator['coderr']
				# addrMode
				self.addrMode = True
				# direction
				self.direction = 0b0
				# op 0
				self.setRegRm(self.operands[0]['data'])
				# op 1
				self.mod = 0b11
				self.setRegReg(self.operands[1]['data'])
			# --------------- reg, mem ---------------
			if self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'mem':
				# opCode
				self.mainOpCode = self.operator['coderm'] # TODO
				# addrMode
				self.addrMode = True # TODO
				# direction
				self.direction = 0b1
				# op 0
				self.setRegReg(self.operands[0]['data'])
				# op 1
				# TODO mem
			# --------------- reg, imd ---------------
			if self.operands[0]['type'] == 'reg' and self.operands[1]['type'] == 'imd':
				# opCode
				self.mainOpCode = self.operator['coderi']
				# addrMode
				self.addrMode = False
				# op 0
				self.setRegReg(self.operands[0]['data'])
				# op 1
				self.setImdData(self.operands[1]['data'], self.operands[0]['data']['size'])
			# --------------- mem, reg ---------------
			if self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'reg':
				# opCode
				self.mainOpCode = self.operator['codemr'] # TODO
				# addrMode
				self.addrMode = True # TODO
				# direction
				self.direction = 0b0
				# op 0
				# TODO mem
				# op 1
				self.setRegReg(self.operands[1]['data'])
			# --------------- mem, mem ---------------
			if self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'mem':
				raise Exception("too many memory references for '" + head + "'")
			# --------------- mem, imd ---------------
			if self.operands[0]['type'] == 'mem' and self.operands[1]['type'] == 'imd':
				# opCode
				self.mainOpCode = self.operator['codemi'] # TODO
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
			if self.operands[0]['type'] == 'imd':
				raise Exception("operand type mismatch for '" + head + "'")
	# ------------------------------ INIT-END ------------------------------

	# ---------------------------- HELPER FUNCS ----------------------------
	def setImdData(self, val, size):
		self.data = [0x00] * (size // 8)
		for i in range(len(self.data)):
			self.data[i] = val & 0xFF
			val >>= 8

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

	# ---------------------------- ASSEMBLY CODE ---------------------------
	@property
	def assemblyCode(self):
		operands = []
		for operand in self.operands:
			if operand['type'] == 'reg':
				operands.append(operand['data']['name'])
			elif operand['type'] == 'mem':
				operands.append('[TODO]') #TODO
			elif operand['type'] == 'imd':
				operands.append(hex(operand['data']))
		return self.operator['name'] + ' ' + ', '.join(operands)
	# ---------------------------- MACHINE CODE ----------------------------
	@property
	def machineCode(self):
		sib = []
		opCode = []		
		addrMode = []
		
		if self.sib:
			sib = [ (self.scale << 6) | (self.index << 3) | (self.base) ]
		else:
			sib = []

		if self.addrMode:
			opCode = [ (self.mainOpCode << 2) | (self.direction << 1) | (self.w) ]
			addrMode = [ (self.mod << 6) | (self.reg << 3) | (self.rm) ]
		else:
			opCode = [ (self.mainOpCode << 4) | (self.w << 3) | (self.reg) ]
			addrMode = []

		return \
			self.prefix + \
			self.rex + \
			opCode + \
			addrMode + \
			sib + \
			self.displacement + \
			self.data

	def toString(self):
		return ' '.join(map("{0:02X}".format, self.machineCode)) + '\t' + self.assemblyCode






