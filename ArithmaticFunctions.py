#########################
#
#    Individual Bits 	#
#
#########################

# Addition of one bit
def ripple_carry_bits(circuit, control_bit, acc_reg, scratch_reg, start_shifting_at):
    """Continue a carry operation
    This assumes that whatever simple op triggered the ripple has already occurred.
    For example, if the ripple started with addition of 1 to the least significant bit,
    manually flip and then call function.
    
    @param circuit: QuantumCircuit containing operands
    @param control_bit: single bit controling whether op begins.
    @param acc_reg: QuantumRegister containing integer to shift
    @param scratch_reg: Quantum registered in initial |0..0> state used to store carry result of each simple addition.
    @param start_shifting_at: index in acc_reg of bit to shift
    """
    
    """
    NOTE: Power is the number of places to shift. Power 1 is controlled by
    control register's 2nd bit, which is control_reg[1]
    and refers to shift of 2^1, or shift one place
    """
    
    # If control_bit, if target bit is |1>, flip carry bit corresponding to target bit.
    circuit.ccx(control_bit, acc_reg[start_shifting_at], scratch_reg[start_shifting_at])
    # If carry bit flipped, flip sum bit after target bit.
    circuit.cx(control_bit, acc_reg[start_shifting_at])
    
    # After flipping target, state |0> means we should have carried... =>
    # before flipping target, state |1> means we should carry.
    
    # Looping through all remaining bits, flip each bit, if it's 1, carry to the next bit, and flip it back.
    for bit in range(start_shifting_at + 1, len(acc_reg)):
        circuit.ccx(acc_reg[bit], scratch_reg[bit - 1], scratch_reg[bit])
        circuit.cx(scratch_reg[bit - 1], acc_reg[bit])

# unconditional addition of one bit
def unconditional_ripple_carry_bits(circuit, acc_reg, scratch_reg, start_shifting_at=0):
    """Continue a carry operation
    This assumes that whatever simple op triggered the ripple has already occurred.
    For example, if the ripple started with addition of 1 to the least significant bit,
    manually flip and then call function.
    
    @param circuit: QuantumCircuit containing operands
    @param acc_reg: QuantumRegister containing integer to shift
    @param scratch_reg: Quantum registered in initial |0..0> state used to store carry result of each simple addition.
    @param start_shifting_at: index in acc_reg of bit to shift
    """
    
    """
    NOTE: Power is the number of places to shift. Power 1 is controlled by
    control register's 2nd bit, which is control_reg[1]
    and refers to shift of 2^1, or shift one place
    """
    
    # If target bit is |1>, flip carry bit corresponding to target bit.
    circuit.cx(acc_reg[start_shifting_at], scratch_reg[start_shifting_at])
    # If carry bit flipped, flip sum bit after target bit.
    circuit.x(acc_reg[start_shifting_at])
    
    # After flipping target, state |0> means we should have carried... =>
    # before flipping target, state |1> means we should carry.
    
    # Looping through all remaining bits, flip each bit, if it's 1, carry to the next bit, and flip it back.
    for bit in range(start_shifting_at + 1, len(acc_reg)):
        circuit.ccx(acc_reg[bit], scratch_reg[bit - 1], scratch_reg[bit])
        circuit.cx(scratch_reg[bit - 1], acc_reg[bit])
        
# def undo_ripple_carry(circuit, control_bit, acc_reg, scratch_reg, start_shifting_at):
#     """
#     Undoes ripple_carry_bits - see documentation above
#     """
#     for bit in range(len(acc_reg) - 1, start_shifting_at + 2, -1):
#         circuit.cx(scratch_reg[bit - 1], acc_reg[bit])
#         circuit.ccx(acc_reg[bit], scratch_reg[bit - 1], scratch_reg[bit])
        
#     circuit.cx(control_bit, acc_reg[start_shifting_at])
#     circuit.ccx(control_bit, acc_reg[start_shifting_at], scratch_reg[start_shifting_at])

# Subtraction of single bit
def c_ripple_subtract(circuit, control_bit, min_reg, scratch_reg, start_shifting_at):
    """Conditionally subtract integer 2^start_shifting_at from min_reg
    
    @param circuit: QuantumCircuit containing operands
    @param control_bit: single bit controling whether all ops occur.
    @param min_reg: QuantumRegister containing integer to transform
    @param scratch_reg: Quantum register in initial |0..0> state used to store carry result of each simple addition.
    @param start_shifting_at: index in acc_reg of bit to shift
    """
    
    circuit.x(min_reg[start_shifting_at])
    circuit.ccx(min_reg[start_shifting_at], control_bit, scratch_reg[start_shifting_at])
    circuit.x(min_reg[start_shifting_at])
    
    # Check how deep the borrow goes. Flip a scratch bit for every borrow op.
    for bit in range(start_shifting_at + 1, len(min_reg)):
        circuit.x(min_reg[bit])
        circuit.ccx(min_reg[bit], scratch_reg[bit - 1], scratch_reg[bit])
        circuit.x(min_reg[bit])
        
    # Perform every borrow indicated in scratch, and then flip targeted bit.
    for bit in range(len(scratch_reg) - 2, -1, -1):
        circuit.cx(scratch_reg[bit], min_reg[bit+1])
        
    # Finally flip original target bit
    circuit.cx(control_bit, min_reg[start_shifting_at])
    
def undo_ripple_borrow(circuit, control_bit, min_reg, scratch_reg, start_shifting_at):
    """Undoes c_ripple_borrow, see documentation"""
    
    circuit.cx(control_bit, min_reg[start_shifting_at])
    for bit in range(len(scratch_reg) - 1):
        circuit.cx(scratch_reg[bit], min_reg[bit+1])
    forward_range = range(start_shifting_at + 1, len(min_reg))
    for bit in range(forward_range.stop - 1, forward_range.start + 1, forward_range.step * (-1)):
        circuit.x(min_reg[bit])
        circuit.ccx(min_reg[bit], scratch_reg[bit - 1], scratch_reg[bit])
        circuit.x(min_reg[bit])
    circuit.x(min_reg[start_shifting_at])
    circuit.ccx(min_reg[start_shifting_at], control_bit, scratch_reg[start_shifting_at])
    circuit.x(min_reg[start_shifting_at])
    

#################################

#	See A new quantum ripple adder
#	arxiv:quant-ph/0410184v1

#################################

def MAJ(circuit, bit_a, bit_b, bit_c):
	"""Compute majority of three inputs and output parity in bit_a."""
	#NOTE: param names consider illustrations in arxiv paper to move
	# in alphabetical order bottom to top.

	circuit.cx(bit_a, bit_b)
	circuit.cx(bit_a, bit_c)
	circuit.ccx(bit_b, bit_c, bit_a)


def UMA(circuit, bit_a, bit_b, bit_c):
	"""UnMajority and Add
	"""
	#NOTE: param names consider illustrations in arxiv paper to move
	# in alphabetical order bottom to top.circuit.x(bit_b)

	circuit.ccx(bit_b, bit_c, bit_a)
	circuit.cx(bit_a, bit_c)
	circuit.cx(bit_c, bit_b)

	# circuit.x(bit_b)
	# circuit.cx(bit_c, bit_b)
	# circuit.ccx(bit_c, bit_b, bit_a)
	# circuit.x(bit_b)
	# circuit.cx(bit_a, bit_c)
	# circuit.cx(bit_a, bit_b)


def CDKM_add(circuit, reg_a, reg_b, scratch):
	"""Compute sum of reg_a and reg_b and put in reg_a
	@param circuit: QuantumCircuit objects involving all other params
	@param reg_a: QuantumRegister containing addend as input and sum as output
	@param reg_b: QuanutmRegister containing addned as input
	@param scratch: two scratch bit register, containing carry control bit and high bit output
	"""

	over_index = len(reg_a)

	MAJ(circuit, reg_a[0], reg_b[0], scratch[0])
	for bit in range(1, over_index):
		MAJ(circuit, reg_a[bit], reg_b[bit], reg_a[bit - 1])

	circuit.cx(reg_a[over_index - 1], scratch[1])

	for bit in range(1, over_index-1):
		UMA(circuit=circuit,
			bit_a=reg_a[over_index - bit],
			bit_b=reg_b[over_index - bit],
			bit_c=reg_a[over_index - bit - 1])
	UMA(circuit=circuit, bit_a=reg_a[0], bit_b=reg_b[0], bit_c=scratch[0])

#################################

#	Operations on two integers	#

#################################

def add_to_b_in_place(circuit, a_reg, b_reg, scratch_reg):
    """|a > | b > => |a > |a+b >
    
    TESTING - Passed minimal test cases July 18 at 8:24am Pacific Time
    """
        
    for bit in range(len(a_reg)):
        circuit.reset(scratch_reg)
        ripple_carry_bits(
            circuit=circuit,
            control_bit=a_reg[bit],
            acc_reg=b_reg,
            scratch_reg=scratch_reg,
            start_shifting_at=bit)
        
def sub_b_from_a_in_place(circuit, minnd_reg, subtrhnd_reg, scratch_reg):
    """Subtract subtrahend integer b from minuend integer a in register a
    
    @param circuit: QuantumCircuit containing other parameters
    @param minnd_reg: QuantumRegister transformed from minuend to difference
    @param subtrhnd_reg: QuantumRegister containing subtrahend
    @param scratch_reg: QuantumRegister in initial |0...0> state used as borrow flags
    for each primitive op (final bit indicates negative difference)
    """
    
    for bit in range(len(subtrhnd_reg)):
        circuit.reset(scratch_reg)
        c_ripple_subtract(
            circuit=circuit,
            control_bit=subtrhnd_reg[bit],
            min_reg=minnd_reg,
            scratch_reg=scratch_reg,
            start_shifting_at=bit)

def bit_shift_left(circuit, register, places=1):
    """
    TESTING - Passed minimal test cases July 21 at 2:30 Pacific Time
    """
    # zero out all trailing bits
    num_bits = len(register)
    for rollover in range(num_bits - places, num_bits):
        circuit.reset(register[rollover])
        
    # swap every bit 'places' forward, with last bits wrapping around to beginning
    if places <= 0:
    	return # irrational behavior if places-1 negative

    for bit in range(num_bits - 1,places-1,-1):
        circuit.swap(register[bit], register[bit - places])
        
def c_copy_register(circuit, control_bit, origin, dest):
    """sets contents of dest with contents of origin if control_bit"""

    circuit.reset(dest)
    for bit in range(len(dest)):
        circuit.ccx(control_bit, origin[bit], dest[bit])
        
def multiply(circuit, multiplicand, multiplier, scratch_zero_check, scratch_carrier, prod_accumulator):
	"""Place product of mulitplicand and multiplier into prod_accumulator
	@param circuit: QuantumCircuit object containing other parameters
	@param mulitiplicand: QuantumRegister containing integer to multiply as input, and |0...0 > as output.
	@param multiplier: QuantumRegister containing integer to multiply
	@param scratch_zero_check: QuantumRegister holds scratch work.
		For every magnitude 1 digit in multiplier, this register will be set to that product of
		multiplicand and then added to accumulated product
	@param scratch_carrier: QuantumRegister used as scratch register for additions"""
    
	c_copy_register(circuit=circuit, control_bit=multiplier[0], origin=multiplicand, dest=prod_accumulator)
    
    
	for bit in range(1, len(multiplier)):
		# free up scratch space
		circuit.reset(scratch_carrier)
		circuit.reset(scratch_zero_check)

		# shift multiplicand one space left, to match magnitude of current multiplier bit
		bit_shift_left(circuit=circuit, register=multiplicand, places=1)

		# copy multiplicand into scratch register only if multiplicand bit, else keep scratch register |0>
		c_copy_register(circuit=circuit, control_bit=multiplier[bit], origin=multiplicand, dest=scratch_zero_check)

		# add that scratch term (shifted multiplicand or zero) to accumulated product
		add_to_b_in_place(circuit=circuit, a_reg=scratch_zero_check, b_reg=prod_accumulator, scratch_reg=scratch_carrier)        

def twos_complement(circuit, reg, scratch_reg):

	for bit in range(len(reg)):
		circuit.x(reg[bit])

	circuit.reset(scratch_reg)

	unconditional_ripple_carry_bits(circuit=circuit,
		acc_reg=reg, scratch_reg=scratch_reg, start_shifting_at=0)

def mod_reduce(circuit, base_reg, mod_reg, scratch_carry, scratch_unadd):
	"""Subtract mod_reg content from base_reg content.
	If base_reg goes negative, add mod back.
    @param circuit: QuantumCircuit containing operands
    @param base_reg: QuantumRegister takes base as input and holds reduced base as output
    @param mod_reg: QuantumRegister takes modulus as input and doesn't change
    @param scratch_carry: QuantumRegister used as scratch work in all steps
    @param scratch_unadd: QuantumRegister scratch register set to 0,
    	or to modulus if sign of base_reg goes negative."""
	
	rollover_index = len(base_reg) - 1

	# # reset register to potentially store subtrahend in case of rollover
	# reset(scratch_unadd)
	
	## Subtraction ##
	twos_complement(circuit, base_reg, scratch_carry)
	add_to_b_in_place(circuit, mod_reg, base_reg, scratch_carry)
	twos_complement(circuit, base_reg, scratch_carry)

	# base_reg now has sign bit. 1 means rollback occurred. Otherwise, do nothing.
	circuit.x(base_reg[rollover_index])
	c_copy_register(circuit, base_reg[rollover_index], mod_reg, scratch_unadd)
	circuit.x(base_reg[rollover_index])
	
	## Re-subtract the given (rolled-over) difference to get the original minuend
	twos_complement(circuit, base_reg, scratch_carry)
	add_to_b_in_place(circuit, scratch_unadd, base_reg, scratch_carry)
	twos_complement(circuit, base_reg, scratch_carry)