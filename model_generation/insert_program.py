# -*- coding: utf-8 -*-

# function: insert_program   
# work: build blocksize list
# made by kjn 2017-01-09

import instMix
import serial
import ILP
import momory as memory
import final


def insert_program(inst_mix, loop_time, basic_block_size, ifelse_pair, serial_block_length, criticalpath, load_global_spatial_length, store_global_spatial_length, load_global_temporal_length, store_global_temporal_length, code_struct_type):
	
	# inst_mix  计算block_size中各种类指令数量的绝对值，block_size是指单个for结构中的指令数量，basic_block_size指if-else结构中单个块的指令数量
	[new_inst_mix, block_size] = instMix.inst_Mix(inst_mix, loop_time, basic_block_size, ifelse_pair, code_struct_type)

	# serial
	[block_inst, new_inst_mix] = serial.serial(new_inst_mix, block_size, serial_block_length)		# lhx  2022.03.09

	# ILP
	[block_inst, new_inst_mix] = ILP.ILP(block_size, criticalpath, new_inst_mix, block_inst)				# lhx

	# memory
	[block_inst_array, new_inst_mix] = memory.memory(new_inst_mix, block_inst, block_size, load_global_spatial_length, store_global_spatial_length, load_global_temporal_length, store_global_temporal_length)  	# lhx  2022.03.09

	# final
	for k in range(len(block_inst_array)):
		block_inst_array[k] = final.final(block_inst_array[k], new_inst_mix, block_size)
		block_free_num = [i for i in range(block_size) if len(block_inst_array[k][i]) == 0]
		assert(len(block_free_num) == 0)

	return block_inst_array