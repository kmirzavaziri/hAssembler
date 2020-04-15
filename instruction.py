table = {
	"add": 0x25,
	"and": 0x42
}


class Instruction:
	head = ""
	data = ""
	def __init__ (self, head, data):
		self.head = head
		self.data = data

	def print(self):
		print(self.head +"\t-\t" + self.data)
	
	def toMachineCode(self):
		if self.head[0] == ';':
			return ''
		if self.head in table:
			return table[self.head]
		raise Exception('Unknown instruction: ' + self.head);
		return ''

