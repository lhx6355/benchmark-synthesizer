# -*- coding: utf-8 -*-


import random


def final(block_inst, inst_mix, block_size):
	simd_inst_num 			= inst_mix['simd_inst_num']
	int_alu_inst_num 		= inst_mix['int_alu_inst_num']
	int_mul_inst_num 		= inst_mix['int_mul_inst_num']
	int_multidiv_inst_num 	= inst_mix['int_multidiv_inst_num']
	fp_neonalu_inst_num 	= inst_mix['fp_neonalu_inst_num']
	fp_neondiv_inst_num 	= inst_mix['fp_neondiv_inst_num']
	fp_neonmul_inst_num 	= inst_mix['fp_neonmul_inst_num']


	block_free_index_array = [index for index in range(block_size) if len(block_inst[index]) == 0]


	assert(simd_inst_num + int_alu_inst_num + int_mul_inst_num + int_multidiv_inst_num + fp_neonalu_inst_num + fp_neondiv_inst_num + fp_neonmul_inst_num <= len(block_free_index_array))


# simd inst insert
	simd_inst_idex = set()
	if simd_inst_num > 0 :
		while len(simd_inst_idex) < simd_inst_num:
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):    			## lhx 2022/03/10
				simd_inst_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10
		simd_inst_idex = list(simd_inst_idex)
		simd_inst_idex.sort()
		for i in range(len(simd_inst_idex)):
			block_inst[simd_inst_idex[i]] = ['dup', 'v6', 'x0']	
	inst_mix['simd_inst_num'] 			= inst_mix['simd_inst_num'] 		- len(simd_inst_idex) 

# fp inst insert
	fp_neonalu_inst_add_idex = set()
	fp_neonalu_inst_sub_idex = set()
	if fp_neonalu_inst_num > 0 :
		while len(fp_neonalu_inst_add_idex) < (fp_neonalu_inst_num / 2):
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				fp_neonalu_inst_add_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10
		fp_neonalu_inst_add_idex = list(fp_neonalu_inst_add_idex)
		fp_neonalu_inst_add_idex.sort()
		for i in range(len(fp_neonalu_inst_add_idex)):
			block_inst[fp_neonalu_inst_add_idex[i]] = ['fadd', 's2', 's1', 's3']

		while len(fp_neonalu_inst_sub_idex) < (fp_neonalu_inst_num - len(fp_neonalu_inst_add_idex)):
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				fp_neonalu_inst_sub_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10
		fp_neonalu_inst_sub_idex = list(fp_neonalu_inst_sub_idex)
		fp_neonalu_inst_sub_idex.sort()
		for i in range(len(fp_neonalu_inst_sub_idex)):
			block_inst[fp_neonalu_inst_sub_idex[i]] = ['fsub', 's2', 's1', 's3']
	inst_mix['fp_neonalu_inst_num'] 	= inst_mix['fp_neonalu_inst_num'] 	- len(fp_neonalu_inst_add_idex) - len(fp_neonalu_inst_sub_idex)


# fp inst insert
	fp_mul_inst_idex = set()
	if fp_neonmul_inst_num > 0 :
		while len(fp_mul_inst_idex) < fp_neonmul_inst_num:
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				fp_mul_inst_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10   
		fp_mul_inst_idex = list(fp_mul_inst_idex)
		fp_mul_inst_idex.sort()
		for i in range(len(fp_mul_inst_idex)):
			block_inst[fp_mul_inst_idex[i]] = ['fmul', 's2', 's1', 's3']
	inst_mix['fp_neonmul_inst_num'] 	= inst_mix['fp_neonmul_inst_num'] 	- len(fp_mul_inst_idex)

	fp_multidiv_inst_idex = set()
	if fp_neondiv_inst_num > 0 :
		while len(fp_multidiv_inst_idex) < fp_neondiv_inst_num:
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				fp_multidiv_inst_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10   
		fp_multidiv_inst_idex = list(fp_multidiv_inst_idex)
		fp_multidiv_inst_idex.sort()
		for i in range(len(fp_multidiv_inst_idex)):
			block_inst[fp_multidiv_inst_idex[i]] = ['fdiv', 's4', 's5', 's6']
	inst_mix['fp_neondiv_inst_num'] 	= inst_mix['fp_neondiv_inst_num'] 	- len(fp_multidiv_inst_idex)



# mul inst insert
	int_mul_inst_idex = set()
	if int_mul_inst_num > 0 :
		while len(int_mul_inst_idex) < int_mul_inst_num:
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				int_mul_inst_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10  
		int_mul_inst_idex = list(int_mul_inst_idex)
		int_mul_inst_idex.sort()
		for i in range(len(int_mul_inst_idex)):
			block_inst[int_mul_inst_idex[i]] = ['smul', 'x16', 'x17', 'x18']
	inst_mix['int_mul_inst_num'] 		= inst_mix['int_mul_inst_num'] 		- len(int_mul_inst_idex)


# muldiv inst insert
	int_multidiv_inst_idex = set()
	if int_multidiv_inst_num > 0 :
		while len(int_multidiv_inst_idex) < int_multidiv_inst_num:
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				int_multidiv_inst_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10   
		int_multidiv_inst_idex = list(int_multidiv_inst_idex)
		int_multidiv_inst_idex.sort()
		for i in range(len(int_multidiv_inst_idex)):
			block_inst[int_multidiv_inst_idex[i]] = ['sdiv', 'w8', 'w9', 'w5']
	inst_mix['int_multidiv_inst_num'] 	= inst_mix['int_multidiv_inst_num'] - len(int_multidiv_inst_idex)


# alu inst insert
	int_alu_inst_add_idex = set()
#	int_alu_inst_sub_idex = set()
	if int_alu_inst_num > 0 :
		while len(int_alu_inst_add_idex) < (int_alu_inst_num / 2):
			index = random.randint(0, len(block_free_index_array) - 1)				## lhx 2022/03/10
			if(len(block_inst[block_free_index_array[index]]) == 0):				## lhx 2022/03/10
				int_alu_inst_add_idex.add(block_free_index_array[index])
				block_free_index_array.remove(block_free_index_array[index])		## lhx 2022/03/10
		int_alu_inst_add_idex = list(int_alu_inst_add_idex)
		int_alu_inst_add_idex.sort()
		for i in range(len(int_alu_inst_add_idex)):
			block_inst[int_alu_inst_add_idex[i]] = ['add', 'w3', 'w4', '#0x01']
	inst_mix['int_alu_inst_num'] 		= inst_mix['int_alu_inst_num'] 		- len(int_alu_inst_add_idex) 


#		while len(int_alu_inst_sub_idex) < (int_alu_inst_num - len(int_alu_inst_add_idex)):
#			index = random.randint(0, block_size - 1)
#			if(len(block_inst[index]) == 0):
#				int_alu_inst_sub_idex.add(index)
#		int_alu_inst_sub_idex = list(int_alu_inst_sub_idex)
#		int_alu_inst_sub_idex.sort()
#		for i in range(len(int_alu_inst_sub_idex)):
#			block_inst[int_alu_inst_sub_idex[i]] = ['sub', 'w3', 'w1', '#0x01']
	len_sub = 0
	for i in range(len(block_inst)):
		if (len(block_inst[i]) == 0):								# 补充 剩余的位置
			block_free_index_array.remove(i)	
			block_inst[i] = ['sub', 'w3', 'w4', '#0x01']
			len_sub += 1

	return block_inst
