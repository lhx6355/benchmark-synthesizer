# -*- coding: utf-8 -*-
# 寄存器依赖距离没有实现，
# 不应该是随机生成
import math
import random

def ILP(block_size, critical_path, inst_mix, block_inst):
    dest_reg = 'w6'
    src_reg  = 'w7'    
    rob_num  = int(block_size / 40)
    critical_path_index = set()

# 由于每条load、store指令需要一条add、sub这种alu指令，因此留给mov的指令数为 int_alu_inst_num - load_inst_num - store_inst_num
    alu_available_inst_num = inst_mix['int_alu_inst_num'] - inst_mix['load_inst_num'] - inst_mix['store_inst_num']
    assert(alu_available_inst_num > 0)   

# use mov to implement criticalpath
    # if critical_path % 2 == 0:
    # critical_path = int(critical_path / 2)                                  # ???为什么除以2
    critical_path_index = random.sample(range(39), critical_path)
    critical_path_index.sort()   
    # critical_path_index = list(range(0, 40))[0 : 40 : int(40 / critical_path)]
    
    # critical_path * rob_num 是 ILP.py 插入的指令总数, 此处判断要插入的指令数量是否超出可用范围
    # to do: 当 alu_available_inst_num 小于 critical_path * rob_num 时，此时会有rob没有被分配到mov指令，关键路径长度维度[0]会增加
    if len(critical_path_index) * rob_num > alu_available_inst_num: 
        rob_num = int(alu_available_inst_num / len(critical_path_index))    # 将alu指令都用来做mov
    for i in range(0, rob_num):
        for j in critical_path_index:                    
            if len(block_inst[j + i * 40]) == 0:                            # 防止覆盖已有的指令， todo: 完善
                block_inst[j + i * 40] = ['mov2', dest_reg, src_reg]
                dest_reg, src_reg = src_reg, dest_reg
                    
    # else:
    #     # critical_path = int(critical_path / 2) + 1
    #     critical_path_index = random.sample(range(39), critical_path)
    #     critical_path_index.sort()
    #     # critical_path_index = list(range(0, 40))[0 : 40 : int(40 / critical_path)]

    #     if len(critical_path_index) * rob_num > alu_available_inst_num:
    #         rob_num = int(alu_available_inst_num / len(critical_path_index))
    #     for i in range(0, rob_num):
    #         for j in critical_path_index[:-1]:
    #             if len(block_inst[j + i * 40]) == 0:
    #                 block_inst[j + i * 40] = ['mov2', dest_reg, src_reg]  
    #                 dest_reg, src_reg = src_reg, dest_reg
    #         block_inst[critical_path_index[-1] + i * 40] = ['and', dest_reg, src_reg]                 # 因为 critical_path 不是 2 的倍数，补充一个关键路径距离
    #         dest_reg, src_reg = src_reg, dest_reg

# to do: calculate the new inst mix, remove the inst used for critical path
    print("    ILP:    int_alu_inst_num : " + str(len(critical_path_index) * rob_num))
    inst_mix['int_alu_inst_num'] = inst_mix['int_alu_inst_num'] - len(critical_path_index) * rob_num
    assert(inst_mix['int_alu_inst_num'] >= 0)

    return block_inst, inst_mix


