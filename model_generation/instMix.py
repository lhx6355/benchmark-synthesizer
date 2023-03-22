# -*- coding: utf-8 -*-
#inst_mix without branch instruction
import math

# input: inst_mix- format: inst ratio without branch
# output: inst_mix- format: inst number without branch
def inst_Mix(inst_mix, loop_time, basic_block_size, ifelse_pair, code_struct_type):
    #block_size = basic_block_size * ifelse_pair
    block_size = block_size_num(code_struct_type, basic_block_size, ifelse_pair)
    # inst_sum = 0
    # for k in inst_mix:
    #     inst_sum += inst_mix[k]
    new_inst_mix = {}
    for k in inst_mix:
        new_inst_mix[k] = int(inst_mix[k] * block_size)  

    inst_num = 0
    for k in inst_mix:
        inst_num = inst_num + new_inst_mix[k]

    if inst_num < block_size:
        new_inst_mix['int_alu_inst_num'] = new_inst_mix['int_alu_inst_num'] + (block_size - inst_num)

    inst_num = 0
    for k in inst_mix:
        inst_num = inst_num + new_inst_mix[k]    

    assert(inst_num == block_size)
    return new_inst_mix, block_size

def block_size_num(code_struct_type, basic_block_size, ifelse_pair):
    block_size = 0
    if code_struct_type == 0:
        block_size = basic_block_size
    elif code_struct_type == 1:
        block_size = basic_block_size
    elif code_struct_type == 2:
        block_size = basic_block_size * ifelse_pair
    elif code_struct_type == 5:
        block_size = basic_block_size
    elif code_struct_type == 6:
        block_size = basic_block_size * ifelse_pair
    elif code_struct_type == 7:
        block_size = basic_block_size * (ifelse_pair + 1)
    return block_size


