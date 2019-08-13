#include <stdio.h>
#include <stdlib.h>
#include <math.h>

const unsigned MOD = 15;
const short DEBUG = 1;

void mod_reduce(unsigned *base_reg, unsigned mod_reg)
{

	unsigned scratch_a = 0; // scratch_b = 0;
	unsigned sign_bit_mask = 1 << (sizeof(unsigned) * 8 - 1);
	unsigned base = *base_reg;
	unsigned unadd_holder = base;
	if(DEBUG){
		printf("Entering Mod Reduce %u Mod %u\n", base, mod_reg);
		printf("Sign bit mask is 0x%x.\n", sign_bit_mask);
	}
	// ## Subtraction ##
	// twos_complement(circuit, base_reg, scratch_carry)
	base = (~base) + 1;
	// add_to_b_in_place(circuit, mod_reg, base_reg, scratch_carry)
	base += mod_reg;
	// twos_complement(circuit, base_reg, scratch_carry)
	base = (~base) + 1;

	if(DEBUG) {
		printf("Base - Modulus = %u\n", base);
		if(sign_bit_mask & base){
			puts("base is negative");
		} else {
			puts("base is not negative, so no further op");
		}
	}

	// # base_reg now has sign bit. 1 means rollback occurred. Otherwise, do nothing.
	// circuit.x(base_reg[rollover_index])
	// c_copy_register(circuit, base_reg[rollover_index], mod_reg, scratch_unadd)
	// circuit.x(base_reg[rollover_index])
	if(sign_bit_mask & base) { // Subtract back if sign is negative, resulting in rollback.

		if(DEBUG) {
			printf("Subtracting minuend (0x%x) from rolled-over 0x%x\n", unadd_holder, base);
		}
	// ## Re-subtract the given (rolled-over) difference to get the original minuend
	// twos_complement(circuit, base_reg, scratch_carry)
	// add_to_b_in_place(circuit, scratch_unadd, base_reg, scratch_carry)
	// twos_complement(circuit, base_reg, scratch_carry)
		base = (~base) + 1;
		base = base + unadd_holder;
		base = (~base) + 1;

	}

	*base_reg = base;
}

/**
 *	Multiplies content of reg by 2^x
 */
void expon_mod_15(unsigned *reg, unsigned x_reg)
{
	unsigned scratch_a = 0, scratch_b = 0, scratch_c = 0;
	unsigned k, j, bit_key;
	unsigned base = *reg;
	short num_shifts;
	printf("\nEntering %u ^ 0x%x Mod %u\n", base, x_reg, MOD);
	for (k = 0; k < 5; k++) { // for each bit in power register
		num_shifts = pow(2, k);
		bit_key = 1 << k;
		if(DEBUG){ 
			printf("Shifting base %d times if key matches.\n", num_shifts);
			printf("Bit key is 0x%x.\n", bit_key);
			if(bit_key & (2 << k)) {
				puts("Match found. Multiplications will apply.");
			} else {
				puts("No match. Multiplications won't apply.");
			}
		}
		for (j=0; j<num_shifts; j++) { // Pattern of copy -- double the copy -- reduce -- copy back 2^power_bit times
			// c_copy_register(qc, control_bit=x_reg[k], origin=base_reg, dest=scratch_a)
			if(x_reg & bit_key) {
				scratch_a = base;
			}
			// bit_shift_left(qc, scratch_a, places=1)
			scratch_a = scratch_a << 1;
			// c_copy_register(qc, control_bit=x_reg[k], origin=scratch_a, dest=base_reg)
			if(x_reg & bit_key) {
				base = scratch_a;
			}
			// flip_fifteen(circ=qc, reg=scratch_a )

			// mod_reduce(
			// 		circuit=qc,
			// 		base_reg=base_reg,
			// 		mod_reg=scratch_a,
			// 		scratch_carry=scratch_b,
			// 		scratch_unadd=scratch_c)

			mod_reduce(&base, MOD);

		}
	}
	*reg = base;
}

int main()
{
	unsigned base, x;
	const char *report_str = "2 ^ %u = %d\n";

	// base = 2;
	// x = 0;
	// expon_mod_15(&base, x);
	// printf(report_str, x, base);

	// base = 2;
	// x = 1;
	// expon_mod_15(&base, x);
	// printf(report_str, x, base);

	// base = 2;
	// x = 2;
	// expon_mod_15(&base, x);
	// printf(report_str, x, base);

	// base = 2;
	// x = 3;
	// expon_mod_15(&base, x);
	// printf(report_str, x, base);

	short i;
	for(i=1; i<2; i++) {

		base = 2;
		expon_mod_15(&base, i);
		printf(report_str, i, base);

	}

	return EXIT_SUCCESS;
}