# -*- coding: utf-8 -*-
import random

class MemoryError(Exception):
    pass

# return the best, medium and worst distribution of memory global temporal locality with fixed memory global spatial locality
""" implement various memory global temporal locality with fixed memory global spatial locality 

    with fixed address distance between adjacent memory accessing instruction, implement various range of global temporal locality;
    e.g.: the best:     address: 0, 4, 0, 4
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
# -1: 后退     0：不变化     1：前进 
def glob_mem_temp(mem_num, global_spatial_length, global_temporal_length):
    MEM_ADDR_MIN = 0x00E80000               
    MEM_ADDR_MAX = 0xEF539000
    MEM_SIZE = MEM_ADDR_MAX - MEM_ADDR_MIN

    # 所有的访存指令的访存地址相同
    if global_temporal_length == 0:
        distribution = [0 % 2 for i in range(mem_num)]
        return distribution
    
    if global_temporal_length == 1:
        loop_inst_num = 2
    else:
        # 相同访存地址之间应该插入奇数个访存指令，
        # 单次循环需要的最小/大指令间隔的指令数量
        min_loop_inst = 2 ** (global_temporal_length - 1)
        max_loop_inst = min((mem_num - 2), 2 ** global_temporal_length - 1)
        if min_loop_inst == max_loop_inst:
            loop_inst_num = min_loop_inst + 1 + 1
        elif min_loop_inst < max_loop_inst:
            loop_inst_num = random.randrange(min_loop_inst, max_loop_inst, 2) + 1 + 1    # 单次 “循环” 中的指令数量，loop_inst_num 是 2 的倍数
        else:
            # 不满足一次循环
            raise MemoryError
        
    deep_step = int(loop_inst_num / 2)
    offset = 8 ** global_spatial_length
    max_offset = deep_step * offset                                                      # 单次循环中，访问最大的地址空间
    if max_offset > MEM_SIZE:
        # 不满足空间分布
        raise MemoryError

    # generate the distribution
    distribution = []
    for i in range(int((mem_num) / loop_inst_num) * loop_inst_num):
        if int(i / deep_step) % 2 == 0:
            distribution.append(1)
        else:
            distribution.append(-1)
            
    return distribution

def inst_allocate(inst_type, inst_mix, block_inst, load_global_spatial_length, load_global_temporal_length):
    if inst_type == 'ldr':
        dest_reg  = 'w14'
        src_reg   = 'x12'
        imme_reg  = 'x10'
        mem_inst_num = inst_mix['load_inst_num']
    elif inst_type == 'str':
        dest_reg  = 'w14'
        src_reg   = 'x13'
        imme_reg  = 'x11'
        mem_inst_num = inst_mix['store_inst_num']
    else:
        return block_inst, inst_mix

    if mem_inst_num == 0:
        return block_inst, inst_mix

    try:
        load_distribution = glob_mem_temp(int(mem_inst_num - 1), load_global_spatial_length, load_global_temporal_length)
    except MemoryError:
        return block_inst, inst_mix

    # 访存地址 0x500000
    immediate_number = 500000           
    int_for_load_num = 0

    # 在开始位置插入一条mov指令
    block_free_index = [i for i in range(len(block_inst)) if len(block_inst[i]) == 0]
    if len(block_free_index) != 0:
        block_inst[block_free_index[0]] = ['mov', src_reg, '#0x' + str(immediate_number)]
        int_for_load_num += 1
        del(block_free_index[0]) 

    load_shift_num = 0
    if load_global_spatial_length != 0:
        # 当偏移小于 8 ** 4，采用立即数偏移，否则采用寄存器立即数偏移
        if load_global_spatial_length <= 4:
            load_offset_imme = int(4 * (random.randint(8 ** (load_global_spatial_length - 1), 8 ** (load_global_spatial_length) - 1) / 4))
        else:
            load_shift_num = (load_global_spatial_length - 2) * 3
            load_offset_imme = int(4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4))
            if len(block_free_index) != 0:
                block_inst[block_free_index[0]] = ['mov', imme_reg, '#' + str(hex(load_offset_imme))]
                int_for_load_num += 1
                del(block_free_index[0]) 
    else:
        load_offset_imme = 0

    # sub指令和load指令插入的位置
    load_inst_index = random.sample(block_free_index, len(load_distribution) * 2 + 1)

    # 插入第一个ldr指令的位置
    load_inst_index.sort()
    block_inst[load_inst_index[0]] = [inst_type, dest_reg, src_reg, '0']
    
    inst_mem_num = 1
    inst_mov_num = 0                                # add sub指令的数量
    for i in range(1, len(load_inst_index), 2):
        # 此时不需要offset的跳转
        if load_distribution[int((i - 1) / 2)] == 0:
            block_inst[load_inst_index[i]] = [inst_type, dest_reg, src_reg, '0']
            inst_mem_num += 1
            continue
        if load_shift_num != 0:
            if load_distribution[int((i - 1) / 2)] == 1:
                block_inst[load_inst_index[i]] = ['add3', src_reg, src_reg, imme_reg, '#' + str(load_shift_num)]
            else:
                block_inst[load_inst_index[i]] = ['sub3', src_reg, src_reg, imme_reg, '#' + str(load_shift_num)]
        else:
            if load_distribution[int((i - 1) / 2)] == 1:
                block_inst[load_inst_index[i]] = ['add2', src_reg, src_reg, '#' + str(hex(load_offset_imme))]
            else:
                block_inst[load_inst_index[i]] = ['sub2', src_reg, src_reg, '#' + str(hex(load_offset_imme))]
        block_inst[load_inst_index[i + 1]] = [inst_type, dest_reg, src_reg, '0']
        inst_mov_num  += 1
        inst_mem_num += 1

    if inst_type == 'ldr':
        inst_mix['load_inst_num'] = inst_mix['load_inst_num'] - inst_mem_num
    elif inst_type == 'str':
        inst_mix['store_inst_num'] = inst_mix['store_inst_num'] - inst_mem_num

    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - inst_mov_num - int_for_load_num

    print("    memory:  " + inst_type + " : " + str(inst_mem_num))

    return block_inst, inst_mix


def memory(inst_mix, block_inst, load_global_spatial_length, store_global_spatial_length, load_global_temporal_length, store_global_temporal_length):
    block_inst, inst_mix = inst_allocate('ldr', inst_mix, block_inst, load_global_spatial_length,  load_global_temporal_length)
    block_inst, inst_mix = inst_allocate('str', inst_mix, block_inst, store_global_spatial_length, store_global_temporal_length)

    return block_inst, inst_mix

# # the inst mix is the new inst returned from function ILP
# def memory_depracated(inst_mix, block_inst, block_size, load_global_spatial_length, store_global_spatial_length):
#     """generate the memory access inst in block inst with assigned global spatial length and implement various global temporal locality
    
#     with block_inst from 
    
#     Arguments:
#         inst_mix {list} -- instruction mix of assigned block size, in the form of integer
#         block_inst {list} -- a full instruction block with fixed block size 
#         block_size {int} -- size of the full instruction block
#         load_global_spatial_length {int} -- load global spatial length
#         store_global_spatial_length {int} -- store global spatial length
    
#     Returns:
#         block_inst_array{list} -- block inst list with load/store instruction, 9 blocks if load/store inst exists, 1 block if load/store inst doesn't exist
#         inst_mix{list} -- inst mix without laod/store inst
#     """
#     MEM_ADDR_MIN = 0xE80000             # memory area bottom boundry                        #  0x81000000   ->   0xE80000              
#     MEM_ADDR_MAX = 0xEF539000           # memory area top boundry

#     load_inst_num = inst_mix['load_inst_num']
#     store_inst_num = inst_mix['store_inst_num']

# #generate global temporal locality distribution
#     try:
#         load_distribution = glob_mem_temp(load_inst_num, load_global_spatial_length)
#         store_distribution = glob_mem_temp(store_inst_num, store_global_spatial_length)
#     except MemoryError:
#         if len(load_distribution) == 0 and len(store_distribution) == 0:
#             block_inst_array = []
#             block_inst_array.append(block_inst)
#             return block_inst_array, inst_mix
#     # print 'debug/momory.py'
#     # print load_distribution

# #initialize the base address register, x12 as base address register for load, x13 for store  
#     immediate_number = 81000000
#     count = 0
#     for index in range(0, len(block_inst)):
#         if(len(block_inst[index]) == 0):
#             block_inst[index] = ['mov', 'x12', '#0x'+str(immediate_number)]
#             break
#     for index in range(0, len(block_inst)):
#         if(len(block_inst[index]) == 0):
#             block_inst[index] = ['mov', 'x13', '#0x'+str(immediate_number)]
#             break    

# #implement the load inst address offset, if spatial length <= 4, use direct offset_imme, else use register(x10), with shift(load_shift_num)
#     load_shift_num = 0
#     if load_global_spatial_length != 0:
#         if load_global_spatial_length <= 4:
#             load_offset_imme = 4 * (random.randint(8 ** (load_global_spatial_length - 1), 8 ** (load_global_spatial_length) - 1) / 4)
#             load_offset_imme = int(load_offset_imme)
#         else:
#             load_shift_num = (load_global_spatial_length -2) * 3
#             load_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
#             load_offset_imme = int(load_offset_imme)
#             for index in range(0, len(block_inst)):
#                 if(len(block_inst[index]) == 0):
#                     block_inst[index] = ['mov', 'x10', '#'+str(hex(load_offset_imme))]
#                     break
#     else:
#         load_offset_imme = 0
# #implement the store inst address offset, if spatial length <= 4, use direct offset_imme, else use register(x10), with shift(store_shift_num)
#     store_shift_num = 0
#     if store_global_spatial_length != 0:
#         if store_global_spatial_length <= 4:
#             store_offset_imme = 4 * (random.randint(8 ** (store_global_spatial_length - 1), 8 ** (store_global_spatial_length) - 1) / 4)
#             store_offset_imme = int(store_offset_imme)
#         else:
#             store_shift_num = (store_global_spatial_length - 2) * 3
#             store_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
#             store_offset_imme = int(store_offset_imme)
#             for index in range(0, len(block_inst)):
#                 if(len(block_inst[index]) == 0):
#                     block_inst[index] = ['mov', 'x11', '#'+str(hex(store_offset_imme))]
#                     break
#     else:
#         store_offset_imme = 0

# #set the load inst position
#     load_inst_index = set()
#     while len(load_inst_index) < load_inst_num:
#         index = random.randint(0, block_size - 1)
#         if(len(block_inst[index]) == 0):    
#             load_inst_index.add(index)
#     load_inst_index = list(load_inst_index)
#     load_inst_index.sort()
# #set the store inst position
#     store_inst_index = set()
#     while len(store_inst_index) < store_inst_num:
#         index = random.randint(0, block_size - 1)
#         if(len(block_inst[index]) == 0):    
#             store_inst_index.add(index)
#     store_inst_index = list(store_inst_index)
#     store_inst_index.sort()

# # set each load/store inst, with best/medium/worst global temporal locality respectively, overall 9 cases
#     temp_1 = block_inst
#     block_inst_array = [[],[],[],[],[],[],[],[],[]]
#     for k in range(len(load_distribution)):
#         block_inst_1 = copy.deepcopy(temp_1)
#         a = 0
#         offset_imme = a
#         load_mov_num = 0
#         for i in range(1, len(load_inst_index)):
#             if load_shift_num != 0:
#                 for j in range(load_inst_index[i-1], load_inst_index[i])[::-1]:
#                     if (len(block_inst_1[j]) == 0): 
#                         if load_distribution[k][i - 1] == 1:
#                             block_inst_1[j] = ['add3', 'x12', 'x12', 'x10', '#'+str(load_shift_num)]
#                         else:
#                             block_inst_1[j] = ['sub3', 'x12', 'x12', 'x10', '#'+str(load_shift_num)]
#                         block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
#                         load_mov_num += 1
#                         break
#             else:
#                 for j in range(load_inst_index[i-1], load_inst_index[i])[::-1]:
#                     if (len(block_inst_1[j]) == 0): 
#                         if load_distribution[k][i - 1] == 1:
#                             block_inst_1[j] = ['add2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
#                         else:
#                             block_inst_1[j] = ['sub2', 'x12', 'x12', '#' + str(hex(load_offset_imme))]
#                         block_inst_1[load_inst_index[i]] = ['ldr', 'w4', 'x12', '0']
#                         load_mov_num += 1
#                         break


#         # shift_num = 0
#         # if store_global_spatial_length != 0:
#         #     if store_global_spatial_length <= 4:
#         #         store_offset_imme = 4 * (random.randint(8 ** (store_global_spatial_length - 1), 8 ** (store_global_spatial_length) - 1) / 4)
#         #     else:
#         #         shift_num = (store_global_spatial_length - 2) * 3
#         #         store_offset_imme = 4 * (random.randint(8 ** (2 - 1), 8 ** (2) - 1) / 4)
#         #         for index in range(0, len(block_inst)):
#         #             if(len(block_inst[index]) == 0):
#         #                 block_inst[index] = ['mov', 'x11', '#'+str(hex(load_offset_imme))]
#         #                 break
#         # else:
#         #     store_offset_imme = 0

# # #set the store inst position
# #         store_inst_index = set()
# #         while len(store_inst_index) < store_inst_num:
# #             index = random.randint(0, block_size - 1)
# #             if(len(block_inst[index]) == 0):    
# #                 store_inst_index.add(index)
# #         store_inst_index = list(store_inst_index)
# #         store_inst_index.sort()
#         temp_2 = block_inst_1
#         for m in range(len(store_distribution)):
#             store_mov_num = 0
#             block_inst_2 = copy.deepcopy(temp_2)
#             offset_imme = a
#             for i in range(1, len(store_inst_index)):
#                 if store_shift_num != 0:
#                     for j in range(store_inst_index[i-1], store_inst_index[i])[::-1]:
#                         if (len(block_inst_2[j]) == 0): 
#                             if store_distribution[m][i - 1] == 1:   
#                                 block_inst_2[j] = ['add3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]
#                             else:
#                                 block_inst_2[j] = ['sub3', 'x13', 'x13', 'x11', '#'+str(store_shift_num)]                            
#                             block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
#                             store_mov_num += 1
#                             break
#                 else:
#                     for j in range(store_inst_index[i-1], store_inst_index[i])[::-1]:
#                         if (len(block_inst_2[j]) == 0): 
#                             if store_distribution[m][i - 1] == 1:
#                                 block_inst_2[j] = ['add2', 'x13', 'x13', '#' + str(hex(store_offset_imme))]
#                             else:
#                                 block_inst_2[j] = ['sub2', 'x13', 'x13', '#' + str(hex(store_offset_imme))]
#                             block_inst_2[store_inst_index[i]] = ['str', 'w2', 'x13', '0']
#                             store_mov_num += 1
#                             break
#             block_inst_array[k * 3 + m] = block_inst_2


# #calculate the new inst_mix
#     inst_mix['load_inst_num'] = inst_mix['load_inst_num'] - len(load_inst_index)
#     inst_mix['store_inst_num'] = inst_mix['store_inst_num'] - len(store_inst_index)
#     inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - load_mov_num - store_mov_num - 4

#     # print 'debug/memory.py'
#     # for i in range(len(block_inst_array[0])):
#     #     print block_inst_array[0][i]

#     return block_inst_array, inst_mix
