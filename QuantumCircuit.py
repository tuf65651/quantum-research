def NOT(arg):
	return 1 - arg

def RESET(arg):
	return 0

class MyQuantumCircuit():

	def __init__(self, register1, register2):
		self.registers = [register1, register2]

	def x(self, register_index):
		register_index = NOT(register_index)

	def cx(self, control, target):
		if(control):
			target = NOT(target)

	def ccx(self, control1, control2, target):
		if(control1 and control2):
			target = NOT(target)

	def swap(self, reference_one, reference_two):
		holder = reference_one
		reference_one = reference_two
		reference_two = holder

	def cswap(self, control, register1, register2):
		if(control):
			self.swap(register1, register2)

	def swap_two_adder(p, q, r, hard_z, hard_one):
		hard_z = RESET(hard_z)
		hard_one = NOT(RESET(hard_one))
		self.cswap(p, hard_z, hard_one)
		self.cswap(q, hard_z, hard_one)
		self.cswap(r, hard_z, hard_one)
		self.cswap(hard_z, r, hard_one)
		self.cswap(q,r, hard_one)