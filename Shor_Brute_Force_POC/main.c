#include <stdio.h>
#include <stdlib.h>
#include <math.h>

const int VEC_LENGTH = 1024;
const int a = 2;
const int N = 25;

int euclid_gcd(long m, long n) {
	int r = m % n;
	while(r != 0){
		m = n;
		n = r;
		r = m % n;
	}
	return (int) n;
}

int* mods_from_range(int start, int stop)
{
	int range = stop - start;
	int *mods = malloc(sizeof(int) * (range + 2));

	int x = 0;
	mods[x] = 1;
	while(x <= range) {
		int next_in = mods[x++]*a;
		mods[x] = next_in % N;
	}
	mods[++x] = -1;

	return mods;
}

int find_freq(int *vec)
{
	int x;
	int second_one = 0, third_one = 0;
	// Linear Search for 1's
	for(x = 0; vec[x] != -1 && second_one == 0; x++) {
		if(vec[x] == 1) second_one = x;
	}

	for( ; vec[x] != -1 && third_one == 0; x++) {
		if(vec[x] == 1) third_one = x;
	}

	if(third_one - second_one != second_one) {
		printf("Problem calculating period.\n");
		printf("Second: %d, Third: %d\n", second_one, third_one );
		int i;
		for(i = 0; i <= third_one; i++) {
			printf("%d ", vec[i]);
		}
		exit(1);
	}

	// int i;
	// for(i = 0; i <= N; i++) {
	// 	printf("%d ", vec[i]);
	// }

	short period = third_one - second_one;
	printf("Found period of %d\n", period);
	printf("%d^%d MOD %d = 1; %d^%d MOD %d = 1;\n", a, second_one, N, a, third_one, N);

	return period;
}

int main()
{
	// Check for lucky guess of a.
	if( !euclid_gcd(a, N)) {
		printf("a = %d is a factor of N = %d.\n", a, N );
	}
	// int aN[2];
	// set_aN(aN);

	// int mods[VEC_LENGTH];
	// mods[0] = 1;
	// int x = 0;
	// while(x < VEC_LENGTH) {
	// 	int next_in = mods[x++]*a;
	// 	mods[x] = next_in % N;
	// }

	int *mods = mods_from_range(0, VEC_LENGTH);

	// x = 0;
	// int second_one = 0, third_one = 0;
	// // Linear Search for 1's
	// while(x < VEC_LENGTH && second_one == 0) {
	// 	if(mods[x] == 1) second_one = x;
	// 	x++;
	// }

	// while(x < VEC_LENGTH && third_one == 0) {
	// 	if(mods[x] == 1) third_one = x;
	// 	x++;
	// }

	// if(third_one - second_one != second_one) {
	// 	printf("Problem calculating period.\n");
	// 	printf("Second: %d, Third: %d\n", second_one, third_one );
	// 	int i;
	// 	for(i = 0; i <= third_one; i++) {
	// 		printf("%d ", mods[i]);
	// 	}
	// 	exit(1);
	// }

	// short period = third_one - second_one;
	// printf("Found period of %d\n", period);
	// printf("%d^%d MOD %d = 1; %d^%d MOD %d = 1;\n", a, second_one, N, a, third_one, N);

	int period = find_freq(mods);

	// Check for odd period
	if( period % 2 ) {
		puts("Can't use odd period. Try a different a-value.\n");
		exit(2);
	}

	// Check for validity of factoring
	long first_remainder = pow(a, period/2) - 1;
	long second_remainder = pow(a, period/2) + 1;

	// Have to check for zero term. Don't remember why.
	if(first_remainder == 0 || second_remainder == 0) {
		printf("Can't have zero factors.\n");
		printf("First term: %ld, Second Term: %ld\n", first_remainder, second_remainder );
		exit(3);
	}

	int first_factor = euclid_gcd(first_remainder, N);
	int second_factor = euclid_gcd(second_remainder, N);

	printf("Found %d and %d\n", first_factor, second_factor);
}