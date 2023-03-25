# -*- coding: utf-8 -*-
import random

def Serial(inst_mix, block_size, serial_block_length):
	block_inst = [[] for i in range(0, block_size)]
	print("    block_inst: inst_num     : " + str(len(block_inst)))
	serial_inst_num = inst_mix['serial_inst_num']
	serial_block_size = random.randint(2 ** (serial_block_length - 1), 2 ** (serial_block_length) - 1)

# set the serial inst position	
	serial_inst_idex = []
	index = random.randint(0, serial_block_size)
	while len(serial_inst_idex) < serial_inst_num and index < block_size:
		if(index < block_size and len(block_inst[index]) == 0 ):
			serial_inst_idex.append(index)
		index += serial_block_size

# implement the serial inst program
	for i in range(len(serial_inst_idex)):
		if int(i / 2) == 0 :
			block_inst[serial_inst_idex[i]] = ['dsb', '#0x0f']
		else :
			block_inst[serial_inst_idex[i]] = ['dmb', '#0x0f']

# caculate the inst mix
	print("    serial: serial_inst_num  : " + str(len(serial_inst_idex)))
	inst_mix['serial_inst_num'] = inst_mix['serial_inst_num'] - len(serial_inst_idex)
	assert(inst_mix['serial_inst_num'] >= 0)

	return block_inst, inst_mix