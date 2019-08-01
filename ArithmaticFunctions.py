
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
    
    pass

def bit_shift_left(circuit, register, places=1):
    """
    TESTING - Passed minimal test cases July 21 at 2:30 Pacific Time
    """
    # zero out all trailing bits
    num_bits = len(register)
    for rollover in range(num_bits - places, num_bits):
        circuit.reset(register[rollover])
        
    # swap every bit 'places' forward, with last bits wrapping around to beginning
    for bit in range(num_bits - 1,places-1,-1):
        circuit.swap(register[bit], register[bit - places])
        
def c_copy_register(circuit, control_bit, origin, dest):
    
    """sets contents of dest with contents of origin if control_bit
    WARNING - perform a reset before use
    """
    circuit.reset(dest)
    for bit in range(len(dest)):
        circuit.ccx(control_bit, origin[bit], dest[bit])
        
def multiply(circuit, multiplicand, multiplier, scratch_zero_check, scratch_carrier, prod_accumulator):
    
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