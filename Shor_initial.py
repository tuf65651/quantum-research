#!/usr/bin/python3

def mods_vector(a, N):

	# assert a less than N
	assert(a < N)

	# build vector to hold returns
	vec = [0] * N
	vec[0] = 1

	# iterate
	for i in range(1,N):
		vec[i] = (a * vec[i-1]) % N

	return vec

def brute_r_from_vec(vec):
	valid_r = [i for i in range(len(vec)) if vec[i] == 1]
	return valid_r[1]

# indeces = [i for i in range(0,371)]
# f_24_371 = mods_vector(24, 371)
# print(indeces[:10])
# print(f_24_371[0:10])
# print()
# print(indeces[75:85])
# print(f_24_371[75:85])
# print()
# print(brute_r_from_vec(f_24_371))

indeces = list(range(0,15))
f_2_15 = mods_vector(2,15)
print(f_2_15)
print()
r = brute_r_from_vec(f_2_15)
