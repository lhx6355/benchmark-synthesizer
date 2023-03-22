# -*- coding: utf-8 -*-

import math
import random
import copy
from turtle import st

class MemoryError(Exception):
    pass

# return the best, medium and worst distribution of memory global temporal locality with fixed memory global spatial locality
def glob_mem_temp(mem_num, global_spatial_length):
    """implement various memory global temporal locality with fixed memory global spatial locality 
    
    with fixed address distance between adjacent memory accessing instruction, implement various range of global temporal locality;
    e.g.: the best: address: 0, 4, 0, 4
          the medium: address: 0, 4, 8, 4, 0, 4, 8
          the worst: address: 0, 4, 8, 12, 16
    need to consider the memory boundry(MEM_ADDR_MIN, MEM_ADDR_MAX)

    Arguments:
        mem_num {int} -- the number of momory instructions, load/store respectively
        global_spatial_length {int} -- address distance of two adjacent memory instrction, used to calculate whether the boundry will be reached
    
    Returns:
        distribution{list} -- list of the best, medium and worst distribution of memory global temporal locality, each emelent is a list in the form of
                              list[0, 1, 0, 1], 0 means minus distance, 1 means plus distance
    
    Raises:
        MemoryError -- raise error if number of memory instruction is 0
    """

    if mem_num == 0:
        raise MemoryError
    else:
        MEM_ADDR_MIN = 0xE80000                               #  0x81000000   ->   0xE80000              
        MEM_ADDR_MAX = 0xEF539000
        MEM_SIZE = MEM_ADDR_MAX - MEM_ADDR_MIN
        distribution = []
        best_distribution = []
        worst_distribution = []
        medium_distribution = []
        mem_num = int(mem_num)
        
        # generate the worst distribution
        offset = 8 ** global_spatial_length                 # lhx : 8 -> 4, 单位为4个字节
        max_num = int(MEM_SIZE / offset)                    # 最大的访存指令数
        if max_num >= mem_num:
            for i in range(int(mem_num)):
                worst_distribution.append(1)
        else:
            loop = int(mem_num / max_num)
            for i in range(loop):
                if i % 2 == 0:
                    for j in range(max_num):
                        worst_distribution.append(1)
                else:
                    for j in range(max_num):
                        worst_distribution.append(0)
            for k in range(max_num * loop, mem_num):
                worst_distribution.append(1 if (loop % 2 == 0) else 0)

        # generate the best distribution
        for i in range(int(mem_num / 2)):
            best_distribution.append(1)
            best_distribution.append(0)
        if mem_num % 2 != 0:
            best_distribution.append(1)

        # generate the medium distribution
        medium = int(math.sqrt(mem_num))
        for i in range(int(mem_num / medium)):
            if i % 2 == 0:
                for j in range(medium):
                    medium_distribution.append(1)
            else:
                for j in range(medium):
                    medium_distribution.append(0)
        for i in range(int(medium * int(mem_num / medium)), mem_num):
            medium_distribution.append(1 if (mem_num / medium % 2 == 0) else 0)

        distribution.append(best_distribution)
        distribution.append(medium_distribution)
        distribution.append(worst_distribution)

        return distribution

def load_inst_allocate(inst_mix, block_inst, block_size, load_global_spatial_length, load_global_temporal_length):
    MEM_ADDR_MIN = 0xE80000                               #  0x81000000   ->   0xE80000              
    MEM_ADDR_MAX = 0xEF539000

    load_inst_num = inst_mix['load_inst_num']

    try:
        load_distribution = glob_mem_temp(load_inst_num, load_global_spatial_length)
    except MemoryError:
        block_inst_array = []
        block_inst_array.append(block_inst)
        return block_inst_array, inst_mix

    immediate_number = 500000
    int_for_load_num = 0

    block_free_index = []
    for i in range(block_size):
        if len(block_inst[i]) == 0:
            block_free_index.append(i)

    for index in range(0, len(block_inst)):
        if(len(block_inst[index]) == 0):
            block_free_index.remove(index)
            block_inst[index] = ['mov', 'x12', '#0x' + str(immediate_number)]
            int_for_load_num += 1
            break

    load_shift_num = 0
    if load_global_spatial_length != 0:
        if load_global_spatial_length <= 4:
            load_offset_imme = 4 * (random.randint(8 ** (load_global_spatial_length - 1), 8 ** (load_global_spatial_length) - 1) / 4)
            load_offset_imme = int(load_offset_imme)
        else:
            load_shift_num = (load_global_spatial_length -2) * 3
            load_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
            load_offset_imme = int(load_offset_imme)
            for index in range(0, len(block_inst)):
                if(len(block_inst[index]) == 0):
                    block_free_index.remove(index)
                    block_inst[index] = ['mov', 'x10', '#' + str(hex(load_offset_imme))]
                    int_for_load_num += 1
                    break
    else:
        load_offset_imme = 0

    load_inst_index = set()
    while len(load_inst_index) < load_inst_num:
        index = random.randint(0, len(block_free_index) - 1)		## lhx 2022/03/10
        if(len(block_inst[block_free_index[index]]) == 0):			## lhx 2022/03/10
            load_inst_index.add(block_free_index[index])
            block_free_index.remove(block_free_index[index])		## lhx 2022/03/10    
    load_inst_index = list(load_inst_index)
    load_inst_index.sort()

    temp_1 = block_inst
    block_inst_array = [[], [], []]
    for k in range(len(load_distribution)):                 # 生成三份，每份依据 load_distribution 而不同 
        block_inst_1 = copy.deepcopy(temp_1)
        load_mov_num = 0
        for i in range(1, len(load_inst_index)):
            if load_shift_num != 0:
                for j in range(load_inst_index[i - 1], load_inst_index[i])[:: -1]:
                    if (len(block_inst_1[j]) == 0):         # 只插入了7000多条指令，并没有插入 load_inst_index 长度的指令
                        if load_distribution[k][i - 1] == 1:
                            block_inst_1[j] = ['add3', 'x12', 'x12', 'x10', '#' + str(load_shift_num)]
                        else:
                            block_inst_1[j] = ['sub3', 'x12', 'x12', 'x10', '#' + str(load_shift_num)]
                        block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
                        load_mov_num += 1
                        break
            else:
                for j in range(load_inst_index[i - 1], load_inst_index[i])[::-1]:
                    if (len(block_inst_1[j]) == 0): 
                        if load_distribution[k][i - 1] == 1:
                            block_inst_1[j] = ['add2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
                        else:
                            block_inst_1[j] = ['sub2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
                        block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
                        load_mov_num += 1
                        break
        block_inst_array[k] = block_inst_1

    inst_mix['load_inst_num'] = inst_mix['load_inst_num'] - load_mov_num
    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - load_mov_num - int_for_load_num

    return block_inst_array, inst_mix

def store_inst_allocate(inst_mix, block_inst, block_size, store_global_spatial_length, store_global_temporal_length):
    MEM_ADDR_MIN = 0xE80000                               #  0x81000000   ->   0xE80000              
    MEM_ADDR_MAX = 0xEF539000

    store_inst_num = inst_mix['store_inst_num']

    try:
        store_distribution = glob_mem_temp(store_inst_num, store_global_spatial_length)
    except MemoryError:
        block_inst_array = []
        block_inst_array.append(block_inst)
        return block_inst_array, inst_mix

    immediate_number = 500000
    int_for_store_num = 0

    block_free_index = []
    for i in range(block_size):
        if len(block_inst[i]) == 0:
            block_free_index.append(i)

    for index in range(0, len(block_inst)):
        if(len(block_inst[index]) == 0):
            block_free_index.remove(index)
            block_inst[index] = ['mov', 'x13', '#0x' + str(immediate_number)]
            int_for_store_num += 1
            break

# implement the store inst address offset, if spatial length <= 4, use direct offset_imme, else use register(x10), with shift(store_shift_num)
    store_shift_num = 0
    if store_global_spatial_length != 0:
        if store_global_spatial_length <= 4:
            store_offset_imme = 4 * (random.randint(8 ** (store_global_spatial_length - 1), 8 ** (store_global_spatial_length) - 1) / 4)
            store_offset_imme = int(store_offset_imme)
        else:
            store_shift_num = (store_global_spatial_length - 2) * 3
            store_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
            store_offset_imme = int(store_offset_imme)
            for index in range(0, len(block_inst)):
                if(len(block_inst[index]) == 0):
                    block_free_index.remove(index)
                    block_inst[index] = ['mov', 'x11', '#'+str(hex(store_offset_imme))]
                    int_for_store_num += 1
                    break
    else:
        store_offset_imme = 0

# set the store inst position
    store_inst_index = set()
    while len(store_inst_index) < store_inst_num:
        index = random.randint(0, len(block_free_index) - 1)				## lhx 2022/03/10
        if(len(block_inst[block_free_index[index]]) == 0):    			    ## lhx 2022/03/10
            store_inst_index.add(block_free_index[index])
            block_free_index.remove(block_free_index[index])		        ## lhx 2022/03/10  
    store_inst_index = list(store_inst_index)
    store_inst_index.sort()

    temp_2 = block_inst
    block_inst_array = [[], [], []]
    for m in range(len(store_distribution)):
        store_mov_num = 0
        block_inst_2 = copy.deepcopy(temp_2)
        for i in range(1, len(store_inst_index)):
            if store_shift_num != 0:
                for j in range(store_inst_index[i - 1], store_inst_index[i])[::-1]:
                    if (len(block_inst_2[j]) == 0): 
                        if store_distribution[m][i - 1] == 1:   
                            block_inst_2[j] = ['add3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]
                        else:
                            block_inst_2[j] = ['sub3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]                            
                        block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
                        store_mov_num += 1
                        break
            else:
                for j in range(store_inst_index[i - 1], store_inst_index[i])[::-1]:
                    if (len(block_inst_2[j]) == 0): 
                        if store_distribution[m][i - 1] == 1:
                            block_inst_2[j] = ['add2', 'x13', 'x13', '#'+str(hex(store_offset_imme))]
                        else:
                            block_inst_2[j] = ['sub2', 'x13', 'x13', '#'+str(hex(store_offset_imme))]
                        block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
                        store_mov_num += 1
                        break
        block_inst_array[m] = block_inst_2

    inst_mix['store_inst_num'] = inst_mix['store_inst_num'] - store_mov_num
    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - store_mov_num - int_for_store_num

    return block_inst_array, inst_mix

def memory(inst_mix, block_inst, block_size, load_global_spatial_length, store_global_spatial_length, load_global_temporal_length, store_global_temporal_length):
    block_inst_array = []
    block_inst_array_1, inst_mix_1 = load_inst_allocate(inst_mix, block_inst, block_size, load_global_spatial_length, load_global_temporal_length)

    for i in range(len(block_inst_array_1)):
        print("    block_inst_array_1 begin : " + str(i))
        new_inst_mix = copy.deepcopy(inst_mix_1)
        block_inst_array_2, inst_mix_2 = store_inst_allocate(new_inst_mix, block_inst_array_1[i], block_size, store_global_spatial_length, store_global_temporal_length)
        block_inst_array.extend(block_inst_array_2)                         # 追加

    return block_inst_array, inst_mix_2

# the inst mix is the new inst returned from function ILP
def memory_depracated(inst_mix, block_inst, block_size, load_global_spatial_length, store_global_spatial_length):
    """generate the memory access inst in block inst with assigned global spatial length and implement various global temporal locality
    
    with block_inst from 
    
    Arguments:
        inst_mix {list} -- instruction mix of assigned block size, in the form of integer
        block_inst {list} -- a full instruction block with fixed block size 
        block_size {int} -- size of the full instruction block
        load_global_spatial_length {int} -- load global spatial length
        store_global_spatial_length {int} -- store global spatial length
    
    Returns:
        block_inst_array{list} -- block inst list with load/store instruction, 9 blocks if load/store inst exists, 1 block if load/store inst doesn't exist
        inst_mix{list} -- inst mix without laod/store inst
    """
    MEM_ADDR_MIN = 0xE80000             # memory area bottom boundry                        #  0x81000000   ->   0xE80000              
    MEM_ADDR_MAX = 0xEF539000           # memory area top boundry

    load_inst_num = inst_mix['load_inst_num']
    store_inst_num = inst_mix['store_inst_num']

#generate global temporal locality distribution
    try:
        load_distribution = glob_mem_temp(load_inst_num, load_global_spatial_length)
        store_distribution = glob_mem_temp(store_inst_num, store_global_spatial_length)
    except MemoryError:
        if len(load_distribution) == 0 and len(store_distribution) == 0:
            block_inst_array = []
            block_inst_array.append(block_inst)
            return block_inst_array, inst_mix
    # print 'debug/momory.py'
    # print load_distribution

#initialize the base address register, x12 as base address register for load, x13 for store  
    immediate_number = 81000000
    count = 0
    for index in range(0, len(block_inst)):
        if(len(block_inst[index]) == 0):
            block_inst[index] = ['mov', 'x12', '#0x'+str(immediate_number)]
            break
    for index in range(0, len(block_inst)):
        if(len(block_inst[index]) == 0):
            block_inst[index] = ['mov', 'x13', '#0x'+str(immediate_number)]
            break    

#implement the load inst address offset, if spatial length <= 4, use direct offset_imme, else use register(x10), with shift(load_shift_num)
    load_shift_num = 0
    if load_global_spatial_length != 0:
        if load_global_spatial_length <= 4:
            load_offset_imme = 4 * (random.randint(8 ** (load_global_spatial_length - 1), 8 ** (load_global_spatial_length) - 1) / 4)
            load_offset_imme = int(load_offset_imme)
        else:
            load_shift_num = (load_global_spatial_length -2) * 3
            load_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
            load_offset_imme = int(load_offset_imme)
            for index in range(0, len(block_inst)):
                if(len(block_inst[index]) == 0):
                    block_inst[index] = ['mov', 'x10', '#'+str(hex(load_offset_imme))]
                    break
    else:
        load_offset_imme = 0
#implement the store inst address offset, if spatial length <= 4, use direct offset_imme, else use register(x10), with shift(store_shift_num)
    store_shift_num = 0
    if store_global_spatial_length != 0:
        if store_global_spatial_length <= 4:
            store_offset_imme = 4 * (random.randint(8 ** (store_global_spatial_length - 1), 8 ** (store_global_spatial_length) - 1) / 4)
            store_offset_imme = int(store_offset_imme)
        else:
            store_shift_num = (store_global_spatial_length - 2) * 3
            store_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
            store_offset_imme = int(store_offset_imme)
            for index in range(0, len(block_inst)):
                if(len(block_inst[index]) == 0):
                    block_inst[index] = ['mov', 'x11', '#'+str(hex(store_offset_imme))]
                    break
    else:
        store_offset_imme = 0

#set the load inst position
    load_inst_index = set()
    while len(load_inst_index) < load_inst_num:
        index = random.randint(0, block_size - 1)
        if(len(block_inst[index]) == 0):    
            load_inst_index.add(index)
    load_inst_index = list(load_inst_index)
    load_inst_index.sort()
#set the store inst position
    store_inst_index = set()
    while len(store_inst_index) < store_inst_num:
        index = random.randint(0, block_size - 1)
        if(len(block_inst[index]) == 0):    
            store_inst_index.add(index)
    store_inst_index = list(store_inst_index)
    store_inst_index.sort()

# set each load/store inst, with best/medium/worst global temporal locality respectively, overall 9 cases
    temp_1 = block_inst
    block_inst_array = [[],[],[],[],[],[],[],[],[]]
    for k in range(len(load_distribution)):
        block_inst_1 = copy.deepcopy(temp_1)
        a = 0
        offset_imme = a
        load_mov_num = 0
        for i in range(1, len(load_inst_index)):
            if load_shift_num != 0:
                for j in range(load_inst_index[i-1], load_inst_index[i])[::-1]:
                    if (len(block_inst_1[j]) == 0): 
                        if load_distribution[k][i - 1] == 1:
                            block_inst_1[j] = ['add3', 'x12', 'x12', 'x10', '#'+str(load_shift_num)]
                        else:
                            block_inst_1[j] = ['sub3', 'x12', 'x12', 'x10', '#'+str(load_shift_num)]
                        block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
                        load_mov_num += 1
                        break
            else:
                for j in range(load_inst_index[i-1], load_inst_index[i])[::-1]:
                    if (len(block_inst_1[j]) == 0): 
                        if load_distribution[k][i - 1] == 1:
                            block_inst_1[j] = ['add2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
                        else:
                            block_inst_1[j] = ['sub2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
                        block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
                        load_mov_num += 1
                        break


        # shift_num = 0
        # if store_global_spatial_length != 0:
        #     if store_global_spatial_length <= 4:
        #         store_offset_imme = 4 * (random.randint(8 ** (store_global_spatial_length - 1), 8 ** (store_global_spatial_length) - 1) / 4)
        #     else:
        #         shift_num = (store_global_spatial_length - 2) * 3
        #         store_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
        #         for index in range(0, len(block_inst)):
        #             if(len(block_inst[index]) == 0):
        #                 block_inst[index] = ['mov', 'x11', '#'+str(hex(load_offset_imme))]
        #                 break
        # else:
        #     store_offset_imme = 0

# #set the store inst position
#         store_inst_index = set()
#         while len(store_inst_index) < store_inst_num:
#             index = random.randint(0, block_size - 1)
#             if(len(block_inst[index]) == 0):    
#                 store_inst_index.add(index)
#         store_inst_index = list(store_inst_index)
#         store_inst_index.sort()
        temp_2 = block_inst_1
        for m in range(len(store_distribution)):
            store_mov_num = 0
            block_inst_2 = copy.deepcopy(temp_2)
            offset_imme = a
            for i in range(1, len(store_inst_index)):
                if store_shift_num != 0:
                    for j in range(store_inst_index[i-1], store_inst_index[i])[::-1]:
                        if (len(block_inst_2[j]) == 0): 
                            if store_distribution[m][i - 1] == 1:   
                                block_inst_2[j] = ['add3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]
                            else:
                                block_inst_2[j] = ['sub3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]                            
                            block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
                            store_mov_num += 1
                            break
                else:
                    for j in range(store_inst_index[i-1], store_inst_index[i])[::-1]:
                        if (len(block_inst_2[j]) == 0): 
                            if store_distribution[m][i - 1] == 1:
                                block_inst_2[j] = ['add2', 'x13', 'x13', '#' + str(hex(store_offset_imme))]
                            else:
                                block_inst_2[j] = ['sub2', 'x13', 'x13', '#' + str(hex(store_offset_imme))]
                            block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
                            store_mov_num += 1
                            break
            block_inst_array[k * 3 + m] = block_inst_2


#calculate the new inst_mix
    inst_mix['load_inst_num'] = inst_mix['load_inst_num'] - len(load_inst_index)
    inst_mix['store_inst_num'] = inst_mix['store_inst_num'] - len(store_inst_index)
    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - load_mov_num - store_mov_num - 4

    # print 'debug/memory.py'
    # for i in range(len(block_inst_array[0])):
    #     print block_inst_array[0][i]

    return block_inst_array, inst_mix
