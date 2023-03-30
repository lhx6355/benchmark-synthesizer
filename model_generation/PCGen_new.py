# -*- coding: UTF-8 -*-
# ------
# Author:
# Email:
# Create: 2016-12-09 by bruceleo92
# Modify: 
# Filename: PCGen_new.py
#
# Description: Pattern Code Generator
# ------

import os
import sys
import pickle

from print_code import print_code
from code_struct import code_struct
from insert_program import insert_program
from code_struct import NotFoundError
import PCGenUtils

def model_generate(pattern_para_list, tr_lib, file_dir):
    BASE_DIR = os.path.dirname(__file__)
    # Instruction mix
    inst_mix = {
            'simd_inst_num':              int(pattern_para_list['InstMix']['SIMDNum']), \
            'load_inst_num':              int(pattern_para_list['InstMix']['LoadInstNum']), \
            'store_inst_num':             int(pattern_para_list['InstMix']['StoreInstNum']), \
            'serial_inst_num':            int(pattern_para_list['InstMix']['SerialInstNum']), \
            'int_alu_inst_num':           int(pattern_para_list['InstMix']['IntAluInstNum']), \
            'int_multidiv_inst_num':      int(pattern_para_list['InstMix']['IntMultiDivNum']), \
            'int_mul_inst_num':           int(pattern_para_list['InstMix']['IntMulNum']), \
            'fp_neonalu_inst_num':        int(pattern_para_list['InstMix']['FpNeonAluNum']), \
            'fp_neondiv_inst_num':        int(pattern_para_list['InstMix']['FpNeonDivNum']), \
            'fp_neonmul_inst_num':        int(pattern_para_list['InstMix']['FpNeonMulNum']), \
            'branch_inst_num':            int(pattern_para_list['InstMix']['BranchInstNum']), \
            }

    # Locality, including instruction locality and memory locality
    inst_fetch_reuse_dist          = int(pattern_para_list['Locality']['InstFetchReuseDist'])
    inst_fetch_addr_dist           = int(pattern_para_list['Locality']['InstFetchAddrDist'])
    load_local_spatial_length      = int(pattern_para_list['Locality']['LoadLocalSpatial'])
    load_global_spatial_length     = int(pattern_para_list['Locality']['LoadGlobalSpatial'])
    load_local_temporal_length     = int(pattern_para_list['Locality']['LoadLocalTemporal'])
    load_global_temporal_length    = int(pattern_para_list['Locality']['LoadGlobalTemporal'])
    store_local_spatial_length     = int(pattern_para_list['Locality']['StoreLocalSpatial'])
    store_global_spatial_length    = int(pattern_para_list['Locality']['StoreGlobalSpatial'])
    store_local_temporal_length    = int(pattern_para_list['Locality']['StoreLocalTemporal'])
    store_global_temporal_length   = int(pattern_para_list['Locality']['StoreGlobalTemporal'])

    # ILP, including register dependence distance and critical path lenth
    critical_path_length           = int(pattern_para_list['ILP']['CriticalPathLength'])
    reg_dependence_length          = int(pattern_para_list['ILP']['RegDependenceLength'])

    # Others
    branch_transition_rate         = float(pattern_para_list['BranchTransitionRate'])
    serial_block_size              = int(pattern_para_list['SerialBlockSize'])

    # generate instruction sum
    inst_sum = 0
    for inst_type in inst_mix:
        inst_sum += inst_mix[inst_type]

    # generate new inst mix- format: ratio without branch   除去分支指令的混合比
    inst_mix_ratio_without_branch = {}
    for inst_type in inst_mix:
        if inst_type != "branch_inst_num":
            inst_mix_ratio_without_branch[inst_type] = float(inst_mix[inst_type]) / float(inst_sum - inst_mix["branch_inst_num"])

#---------------------------------------*************************-------------------------------------------
# the complete flow of generate a model according  to json file
    if store_global_spatial_length > 10 or load_global_spatial_length > 10 :                                  # lhx
        raise NotFoundError
    

#---------------------------------------*************************-------------------------------------------
    # select the matching code structure
    try:
        code_struct_para = code_struct(tr_lib, inst_mix, branch_transition_rate, inst_fetch_reuse_dist, inst_fetch_addr_dist)
    except NotFoundError:
        raise NotFoundError
    else:
        basic_block_size = code_struct_para['basic_block_size']
        loop_time        = code_struct_para['loop_time']
        ifelse_pair      = code_struct_para['ifelse_pair']
        code_type        = code_struct_para['code_struct_type']

        try:
            block_inst = insert_program(inst_mix_ratio_without_branch, loop_time, basic_block_size, ifelse_pair, serial_block_size, critical_path_length, \
                    load_global_spatial_length, store_global_spatial_length, load_global_temporal_length, store_global_temporal_length, code_type)
        except NotFoundError:
            raise NotFoundError
        else:
            fout = open(os.path.join(BASE_DIR, file_dir), 'w')
            fname = 'func' + os.path.basename(file_dir).split('.')[0]
            print_code(code_struct_para, block_inst, fname, fout)
            fout.close()

def PCGen_new():
    BASE_DIR = os.path.dirname(__file__)
    gv = PCGenUtils.commandline_parser()                             # 获取json文件里的参数，创建输出C程序的文件夹

    # load the code structure library                                 # 读取创建的分支跳转模板库
    print ('step 0: loading code structure library')
    tr_file = open(os.path.join(BASE_DIR, "TRLib_new.pkl"), 'rb')
    tr_lib = pickle.load(tr_file)
    tr_file.close()

    # generate model file
    # flag = 0
    for pl in range(gv['process_loops']):                           # 输入了几个参数json文件就循环几次
        print ('loops ' + os.path.basename(gv['code_files'][pl]) + ': ')
        # if os.path.basename(gv['code_files'][pl]) == "96583.c" or flag == 1:
            # flag = 1
        try:
            model_generate(gv['ppls'][pl], tr_lib, gv['code_files'][pl])
        except NotFoundError:
            os.remove(os.path.join(BASE_DIR, gv['pattern_files'][pl]))                      # 删除未被使用的json文件, 使得最后生成的c文件的数量与json文件一致
            continue

if __name__ == '__main__':
    sys.argv.append("--ifd")
    sys.argv.append("PatternFiles")
    sys.argv.append("--ofd")
    sys.argv.append("CodeFiles")

    PCGen_new()
