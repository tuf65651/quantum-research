"""Implementation of Shor's Algorithm using Qiskit and QASN simulator."""
"""All code by Shmuel Jacobs, algorithms as cited
Circuit is hard coded for specific case a=2, N=21
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from datetime import datetime

REG_SIZE=6
from ArithmaticFunctions import *

backend = Aer.get_backend("qasm_simulator")

x_reg = QuantumRegister(5, 'x') # register holds superposition of powers, to which a is raised.
base_reg = QuantumRegister(REG_SIZE, 'base') # Evaluate a^x in this register
scratch_a = QuantumRegister(REG_SIZE, 'sca') 
# Three scratch registers are needed. Each addition requires one carry register.
# Each multiplication requires additions, a register to hold conditional sum, and product accumulator.
# Multiplications as bitshifts require additions, conditional subtrahend and conditional shift value.
scratch_b = QuantumRegister(REG_SIZE, 'scb')
scratch_c = QuantumRegister(REG_SIZE, 'scc')
class_reg = ClassicalRegister(REG_SIZE, 'y')
qc = QuantumCircuit(x_reg, base_reg, scratch_a, scratch_b, class_reg)

def qft(circ, q, n):
    """n-bit QFT on q in circ"""
    for j in range(n):
        circ.h(q[j])
        for k in range(j+1, n):
            circ.cu1(math.pi/float(2**(k-j)), q[k], q[j])
        circ.barrier()

def flip_twentyone(circ, reg):

	circ.x(reg[5])
	circ.x(reg[3])
	circ.x(reg[0])

def flip_fifteen(circ, reg):

	for bit in range(4):
		circ.x(reg[bit])

def main():

	qft(qc, x_reg, 6)

	#### Implement Exponentiation as a series of modular multiplications, Neilsen and Chang style
	# NOTE: Selection of 2 as base allows bit shifts of one instead of multiplying base**i
	# to prepare each exponential term. 2 is a suitable base for factoring 15 and 21, but is not 
	# always suitable. All multiplication by a power of two can be implemented as a bitshift.

	"""When using base that is not a square integer, implement each multiplication by x^i using the following.
		- Set scratch register to 1.
		- c_copy original base (constant a in Neilsen and Chuang description) into scratch register.
		- For j in 0:log2(i)
			- multiply scratch register by itself
			- mod reduce
	"""
	
	# Set base to 1
	qx.x(base_reg[0])

	# When x[0], multiply base by 2 (base *= x^1, implemented as overwrite to 2), else no op.
	# This is a shortcut for 2^1 to cut down on multiplications.
	qc.reset(scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=base_reg, dest=scratch_a)
	bit_shift_left(qc, scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=scratch_a, dest=base_reg)

	#### If x[1], double 2 times

	# Copy into scratch register to double twice
	qc.reset(scratch_a)
	c_copy_register(qc, control_bit=x_reg[0], origin=base_reg, dest=scratch_a)
	bit_shift_left(qc, scratch_a, places=2)
	# Max value of scratch_a at this point is 2^3. Since period is not known,
	# all future shifts are immediately followed by mod reduction.

	#### Optimized multiplications are over. Define general case for a=2.

	#### If x[k], mod double base_reg 2^(k+1) times
	for k in range(2, len(x_reg)):
		for j in range(2**k): # Pattern of copy -- double the copy -- reduce -- copy back
			c_copy_register(qc, control_bit=x_reg[k], origin=base_reg, dest=scratch_a)
			bit_shift_left(qc, scratch_a, places=1)
			c_copy_register(qc, control_bit=x_reg[k], origin=scratch_a, dest=base_reg)
			flip_fifteen(circ=qc, reg=scratch_a )
			mod_reduce(
					circuit=qc,
					base_reg=base_reg,
					mod_reg=scratch_a,
					scratch_carry=scratch_b,
					scratch_unadd=scratch_c)
