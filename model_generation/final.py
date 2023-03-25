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


	block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]


	assert(simd_inst_num + int_alu_inst_num + int_mul_inst_num + int_multidiv_inst_num + fp_neonalu_inst_num + fp_neondiv_inst_num + fp_neonmul_inst_num <= len(block_free_index))

# simd inst insert
	if simd_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		simd_inst_idex = random.sample(block_free_index, simd_inst_num)
		for i in simd_inst_idex:
			block_inst[i] = ['dup', 'v6', 'x0']	
		inst_mix['simd_inst_num'] 			= inst_mix['simd_inst_num'] 		- len(simd_inst_idex) 

# fp inst insert
	if fp_neonalu_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		fp_neonalu_inst_add_idex = random.sample(block_free_index, int(fp_neonalu_inst_num / 2))
		for i in fp_neonalu_inst_add_idex:
			block_inst[i] = ['fadd', 's2', 's1', 's3']

		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		fp_neonalu_inst_sub_idex = random.sample(block_free_index, fp_neonalu_inst_num - len(fp_neonalu_inst_add_idex))
		for i in fp_neonalu_inst_sub_idex:
			block_inst[i] = ['fsub', 's2', 's1', 's3']
		inst_mix['fp_neonalu_inst_num'] 	= inst_mix['fp_neonalu_inst_num'] 	- len(fp_neonalu_inst_add_idex) - len(fp_neonalu_inst_sub_idex)

# fp mul insert
	if fp_neonmul_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		fp_mul_inst_idex = random.sample(block_free_index, fp_neonmul_inst_num)
		for i in fp_mul_inst_idex:
			block_inst[i] = ['fmul', 's2', 's1', 's3']
		inst_mix['fp_neonmul_inst_num'] 	= inst_mix['fp_neonmul_inst_num'] 	- len(fp_mul_inst_idex)

# fp muldiv insert
	if fp_neondiv_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]			
		fp_multidiv_inst_idex = random.sample(block_free_index, fp_neondiv_inst_num)
		for i in fp_multidiv_inst_idex:
			block_inst[i] = ['fdiv', 's4', 's5', 's6']
		inst_mix['fp_neondiv_inst_num'] 	= inst_mix['fp_neondiv_inst_num'] 	- len(fp_multidiv_inst_idex)

# mul inst insert
	if int_mul_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]	
		int_mul_inst_idex = random.sample(block_free_index, int_mul_inst_num)
		for i in int_mul_inst_idex:
			block_inst[i] = ['smul', 'x16', 'x17', 'x18']
		inst_mix['int_mul_inst_num'] 		= inst_mix['int_mul_inst_num'] 		- len(int_mul_inst_idex)

# muldiv inst insert
	if int_multidiv_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		int_multidiv_inst_idex = random.sample(block_free_index, int_multidiv_inst_num)
		for i in int_multidiv_inst_idex:
			block_inst[i] = ['sdiv', 'w8', 'w9', 'w5']
		inst_mix['int_multidiv_inst_num'] 	= inst_mix['int_multidiv_inst_num'] - len(int_multidiv_inst_idex)

# alu inst insert
	if int_alu_inst_num > 0 :
		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		int_alu_inst_add_idex = random.sample(block_free_index, int(int_alu_inst_num / 2))
		for i in int_alu_inst_add_idex:
			block_inst[i] = ['add', 'w3', 'w4', '#0x01']

		block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
		int_alu_inst_sub_idex = random.sample(block_free_index, int_alu_inst_num - len(int_alu_inst_add_idex))
		for i in int_alu_inst_sub_idex:
			block_inst[i] = ['sub', 'w3', 'w4', '#0x01']
		inst_mix['int_alu_inst_num'] 		= inst_mix['int_alu_inst_num'] 		- len(int_alu_inst_add_idex) - len(int_alu_inst_sub_idex) 
# 
	block_free_index = [index for index in range(block_size) if len(block_inst[index]) == 0]
	for i in block_free_index:
		block_inst[i] = ['add', 'w3', 'w4', '#0x01']

	return block_inst, inst_mix
