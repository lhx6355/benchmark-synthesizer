# -*- coding: utf-8 -*-


import math

class NotFoundError(Exception):
    pass

# function to select the matching code structure based on instruction mix, branch transition rate, instruction fetch reuse distance and instruction fetch address distance
# @profile
def code_struct(tr_lib, inst_mix, branch_transition_rate, inst_fetch_reuse_dist, inst_fetch_addr_dist, \
                load_local_temporal, load_global_temporal, store_local_temporal, store_global_temporal):    

    # define the error for selection step
    RATIO_ERROR_MIN = 0.9
    RATIO_ERROR_MAX = 1.1

    # get the branch instruction number and instruction sum
    branch_inst_num = inst_mix['branch_inst_num']
    inst_sum = 0
    for k in inst_mix:
        inst_sum += inst_mix[k]
    basic_block_size = inst_sum
    if branch_inst_num != 0:
        basic_block_size = int(round(float(inst_sum) / float(branch_inst_num)))
    
    # search tr_lib for matching code structure
    selected_lib_key = [0, 0, 0, 0, 0, 0]
    for lib_key in tr_lib:
        # lib_code_struct_type = lib_key[0]
        # lib_branch_inst_num = lib_key[1]
        # lib_branch_transition_rate = lib_key[2]
        # lib_loop_time = lib_key[3]
        # lib_ifelse_pair = lib_key[4]
        # lib_embedded_loop_time = lib_key[5]
        # basic_block_size = basic_block(lib_code_struct_type, lib_loop_time, lib_ifelse_pair, lib_embedded_loop_time, inst_sum)
        # print 'basic block size: ' + str(basic_block_size)
        # branch_transition_rate_err = abs(lib_key[2] - branch_transition_rate)

# to-do: fix the zero division exception
        # branch_inst_num_ratio = 0
        if branch_inst_num != 0:
            branch_inst_num_ratio = float(lib_key[1]) / float(branch_inst_num)
        elif lib_key[1] != 0:
            branch_inst_num_ratio = 0
        else:
            branch_inst_num_ratio = 1
            continue

        if abs(lib_key[2] - branch_transition_rate) < 0.1 and \
            branch_inst_num_ratio > RATIO_ERROR_MIN and \
            branch_inst_num_ratio < RATIO_ERROR_MAX :
            lib_code_struct_type    = lib_key[0] 
            lib_ifelse_pair         = lib_key[4]
            lib_embedded_loop_time  = lib_key[5]
            lib_inst_fetch_reuse_dist, undefined = inst_locality(basic_block_size, lib_code_struct_type, \
                                                                     lib_ifelse_pair, lib_embedded_loop_time)
            if abs(lib_inst_fetch_reuse_dist[0] - inst_fetch_reuse_dist) == 0:
                print ('    code_struct: find the matching structure')
                selected_lib_key = lib_key
                break

# store and output the code structure
    if selected_lib_key == [0, 0, 0, 0, 0, 0]:
        raise NotFoundError
    else:
        code_struct_para = {}
        code_struct_para['code_struct_type']    = selected_lib_key[0]
        code_struct_para['loop_time']           = selected_lib_key[3]
        code_struct_para['ifelse_pair']         = selected_lib_key[4]
        code_struct_para['embedded_loop_time']  = selected_lib_key[5]
        code_struct_para['basic_block_size']    = basic_block_size
        code_struct_para['modulos']             = tr_lib[selected_lib_key][0]
        code_struct_para['ismoduled']           = tr_lib[selected_lib_key][1]
        return code_struct_para

# return the locality parameter of given code structure
def inst_locality(basic_block_size, code_struct_type, ifelse_pair, embedded_loop_time):
    FETCH_REUSE_DIST_MAX = 10
    LOOP_SUFFIX_INST_NUM = 6

    inst_fetch_reuse_dist = []
    inst_fetch_addr_dist = []
    if code_struct_type == 0:
        dist1 = FETCH_REUSE_DIST_MAX
        inst_fetch_reuse_dist.append(dist1)
    elif code_struct_type == 1:
        dist1 = int(math.ceil(math.log(basic_block_size + LOOP_SUFFIX_INST_NUM, 2)))
        inst_fetch_reuse_dist.append(dist1)
    elif code_struct_type == 2:
        dist1 = FETCH_REUSE_DIST_MAX
        inst_fetch_reuse_dist.append(dist1)
    elif code_struct_type == 5:
        dist1 = int(math.ceil(math.log(basic_block_size + LOOP_SUFFIX_INST_NUM, 2)))
        dist2 = int(math.ceil(math.log(LOOP_SUFFIX_INST_NUM * 2 + basic_block_size, 2)))
        inst_fetch_reuse_dist.append(dist1)
        inst_fetch_reuse_dist.append(dist2)
    elif code_struct_type == 6:
        dist1 = int(math.ceil(math.log((basic_block_size + 4) * ifelse_pair + LOOP_SUFFIX_INST_NUM, 2)))
        inst_fetch_reuse_dist.append(dist1)
    elif code_struct_type == 7:
        dist1 = int(math.ceil(math.log(basic_block_size + LOOP_SUFFIX_INST_NUM, 2)))            # 内部for循环的
        dist2 = int(math.ceil(math.log((basic_block_size + 4) * ifelse_pair + LOOP_SUFFIX_INST_NUM + basic_block_size * embedded_loop_time + LOOP_SUFFIX_INST_NUM, 2)))
        inst_fetch_reuse_dist.append(dist1)
        inst_fetch_reuse_dist.append(dist2)
    return inst_fetch_reuse_dist, inst_fetch_addr_dist

# calculate the basic_block_size according to the code structure parameter and input json data
def basic_block(code_struct_type, loop_time, ifelse_pair, embedded_loop_time, inst_sum):
    LOOP_SUFFIX_INST_NUM = 6
    IFELSE_SUFFIX_INST_NUM = 4
    basic_block_size = 0
    if code_struct_type == 0:
        basic_block_size = inst_sum
    elif code_struct_type == 1:
        basic_block_size = int(round((inst_sum - LOOP_SUFFIX_INST_NUM * embedded_loop_time) / float(embedded_loop_time)))
    elif code_struct_type == 2:
        basic_block_size = int(round((inst_sum - IFELSE_SUFFIX_INST_NUM * ifelse_pair) / float(ifelse_pair)))
    elif code_struct_type == 5:
        basic_block_size = int(round((inst_sum - LOOP_SUFFIX_INST_NUM * (loop_time * (embedded_loop_time + 1))) / float((loop_time * embedded_loop_time))))
    elif code_struct_type == 6:
        basic_block_size = int(round((inst_sum - (IFELSE_SUFFIX_INST_NUM * ifelse_pair + LOOP_SUFFIX_INST_NUM) * loop_time) / float((ifelse_pair * loop_time))))
    elif code_struct_type == 7:
        basic_block_size = int(round((inst_sum - IFELSE_SUFFIX_INST_NUM * ifelse_pair * loop_time - LOOP_SUFFIX_INST_NUM * (loop_time * (embedded_loop_time + 1))) / float(((ifelse_pair + embedded_loop_time) * loop_time))))

    # if basic_block_size <= 0:
    #     raise NotFoundError
    # else:
    #     return basic_block_size
    return basic_block_size

