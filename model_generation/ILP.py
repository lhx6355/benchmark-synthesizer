# -*- coding: utf-8 -*-
# 寄存器依赖距离没有实现，
# 不应该是随机生成
import math
import random

def ILP(block_size, critical_path, inst_mix, block_inst):
    dest_reg = 'w6'
    src_reg  = 'w7'    
    ROB_SIZE = 40
    rob_num  = int(block_size / ROB_SIZE)
    critical_path_index = set()

# 由于每条load、store指令需要一条add、sub这种alu指令，因此留给mov的指令数为 int_alu_inst_num - load_inst_num - store_inst_num
    alu_available_inst_num = inst_mix['int_alu_inst_num'] - inst_mix['load_inst_num'] - inst_mix['store_inst_num']
    assert(alu_available_inst_num > 0)   

# use mov to implement criticalpath
    # if critical_path % 2 == 0:
    critical_path_index = random.sample(range(39), critical_path)
    critical_path_index.sort()   
    # 此时 criticalpath 不再等于 len(critical_path_index)
    # critical_path_index = list(range(0, ROB_SIZE))[0 : ROB_SIZE : int(ROB_SIZE / critical_path)]
    
    # len(critical_path_index) * rob_num 是 ILP.py 插入的指令总数, 此处判断要插入的指令数量是否超出可用范围
    if len(critical_path_index) * rob_num > alu_available_inst_num: 
        rob_num = int(alu_available_inst_num / len(critical_path_index))    # 将alu指令都用来做mov
    for i in range(0, rob_num):
        for j in critical_path_index:                    
            if len(block_inst[j + i * ROB_SIZE]) == 0:                            # 防止覆盖已有的指令， todo: 完善
                block_inst[j + i * ROB_SIZE] = ['mov', dest_reg, src_reg]
                dest_reg, src_reg = src_reg, dest_reg
    
    # 当插入的 mov 指令的数量为奇数个时，在最后的位置补充一个关键路径距离
    if len(critical_path_index) * rob_num % 2 != 0:
        index = rob_num * ROB_SIZE
        while(index < block_size):
            if(len(block_inst[index]) == 0):
                block_inst[index] = ['mov', dest_reg, src_reg] 
                dest_reg, src_reg = src_reg, dest_reg
                break
            else:
                index = block_inst + 1                  

    print("    ILP:    int_alu_inst_num : " + str(len(critical_path_index) * rob_num))
    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - len(critical_path_index) * rob_num
    assert(inst_mix['int_alu_inst_num'] >= 0)

    return block_inst, inst_mix


