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
import random
import shutil

from print_code import print_code
from code_struct import code_struct
from insert_program import insert_program
from code_struct import NotFoundError
import PCGenUtils as pgu

class PCGenCore(object):
    ppl = None
    code_list = None

# 初始化: 导入json参数 
    def __init__(self, pattern_para_list):
        self.ppl = pattern_para_list
        # Instruction mix
        self.inst_mix = {
                'simd_inst_num':              int(self.ppl['InstMix']['SIMDNum']), \
                'load_inst_num':              int(self.ppl['InstMix']['LoadInstNum']), \
                'store_inst_num':             int(self.ppl['InstMix']['StoreInstNum']), \
                'serial_inst_num':            int(self.ppl['InstMix']['SerialInstNum']), \
                'int_alu_inst_num':           int(self.ppl['InstMix']['IntAluInstNum']), \
                'int_multidiv_inst_num':      int(self.ppl['InstMix']['IntMultiDivNum']), \
                'int_mul_inst_num':           int(self.ppl['InstMix']['IntMulNum']), \
                'fp_neonalu_inst_num':        int(self.ppl['InstMix']['FpNeonAluNum']), \
                'fp_neondiv_inst_num':        int(self.ppl['InstMix']['FpNeonDivNum']), \
                'fp_neonmul_inst_num':        int(self.ppl['InstMix']['FpNeonMulNum']), \
                'branch_inst_num':            int(self.ppl['InstMix']['BranchInstNum']), \
                }

        # Locality, including instruction locality and memory locality
        self.inst_fetch_reuse_dist          = int(self.ppl['Locality']['InstFetchReuseDist'])
        self.inst_fetch_addr_dist           = int(self.ppl['Locality']['InstFetchAddrDist'])
        self.load_local_spatial_length      = int(self.ppl['Locality']['LoadLocalSpatial'])
        self.load_global_spatial_length     = int(self.ppl['Locality']['LoadGlobalSpatial'])
        self.load_local_temporal_length     = int(self.ppl['Locality']['LoadLocalTemporal'])
        self.load_global_temporal_length    = int(self.ppl['Locality']['LoadGlobalTemporal'])
        self.store_local_spatial_length     = int(self.ppl['Locality']['StoreLocalSpatial'])
        self.store_global_spatial_length    = int(self.ppl['Locality']['StoreGlobalSpatial'])
        self.store_local_temporal_length    = int(self.ppl['Locality']['StoreLocalTemporal'])
        self.store_global_temporal_length   = int(self.ppl['Locality']['StoreGlobalTemporal'])

        # ILP, including register dependence distance and critical path lenth
        self.critical_path_length           = int(self.ppl['ILP']['CriticalPathLength'])
        self.reg_dependence_length          = int(self.ppl['ILP']['RegDependenceLength'])

        # Others
        self.branch_transition_rate         = float(self.ppl['BranchTransitionRate'])
        self.serial_block_size              = int(self.ppl['SerialBlockSize'])

        # generate instruction sum
        self.inst_sum = 0
        for inst_type in self.inst_mix:
            self.inst_sum += self.inst_mix[inst_type]

        # generate new inst mix- format: ratio without branch   除去分支指令的混合比
        self.inst_mix_ratio_without_branch = {}
        for inst_type in self.inst_mix:
            if inst_type != "branch_inst_num":
                self.inst_mix_ratio_without_branch[inst_type] = float(self.inst_mix[inst_type]) / float(self.inst_sum - self.inst_mix["branch_inst_num"])


    # the complete flow of generate a model according  to json file
    def model_generate(self, tr_lib, file_dir):
        if self.store_global_spatial_length > 10 or self.load_global_spatial_length > 10 :                                  # lhx
            return
        # select the matching code structure
        try:
            code_struct_para = code_struct(tr_lib, self.inst_mix, self.branch_transition_rate, self.inst_fetch_reuse_dist, \
                            self.inst_fetch_addr_dist, self.load_local_temporal_length, self.load_global_temporal_length, \
                            self.store_local_temporal_length, self.store_global_temporal_length)
        except NotFoundError:
            raise NotFoundError
        else:
            fout = open(file_dir, 'w')
            basic_block_size = code_struct_para['basic_block_size']
            loop_time        = code_struct_para['loop_time']
            ifelse_pair      = code_struct_para['ifelse_pair']
            code_type        = code_struct_para['code_struct_type']

            block_inst = insert_program(self.inst_mix_ratio_without_branch, loop_time, basic_block_size, ifelse_pair, self.serial_block_size, self.critical_path_length, \
                    self.load_global_spatial_length, self.store_global_spatial_length, self.load_global_temporal_length, self.store_global_temporal_length, code_type)

            # 随机的选择了一个block输出
            # selected_block_inst_index = random.randint(0, len(block_inst) - 1)
            filename = file_dir.split('/')
            func_name = 'func' + filename[-1].split('.')[0]
            print_code(code_struct_para, block_inst, func_name, fout)
            print ('    done!!!!')
            fout.close()


''' gv = dict{                     # Global Values
                pattern_files: [], # input pattern parameters file
                code_files: [],    # output C/C++ source code file
                process_loops: 0,  # N = 'Number of parameter files to process'
                ppls: [],          # Pattern Parameters ListS                       json
'''
def PCGen_new():
    gv = pgu.commandline_parser()
    pgu.patterninput_parser(gv)             # 获取json文件里的参数

    # delete all the old files
    BASE_DIR = os.path.dirname(__file__)
    dest_dir = os.path.join(BASE_DIR, 'CodeFiles')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)                                     # 递归删除文件夹下的所有子文件夹和子文件
    os.mkdir(dest_dir)                                              # 创建 CodeFiles 文件夹

    # load the code structure library                               # 读取创建的分支跳转模板库
    print ('step 0: loading code structure library')
    tr_file = open(os.path.join(BASE_DIR, "TRLib_new.pkl"), 'rb')
    tr_lib = pickle.load(tr_file)

    # generate model file
    # flag = 0
    for pl in range(gv['process_loops']):                           # 输入了几个参数json文件就循环几次
        print ('loops ' + gv['code_files'][pl].split('/')[-1] + ': ')
        # if gv['code_files'][pl].split('/')[-1] == "96583.c" or flag == 1:
        # flag = 1
        pgc = PCGenCore(gv['ppls'][pl])                             # 参数传给 PCGenCore 类
        file_dir = gv['code_files'][pl]
        try:
            pgc.model_generate(tr_lib, file_dir)
        except NotFoundError:
            continue

    tr_file.close()

if __name__ == '__main__':
    sys.argv.append("--ifd")
    sys.argv.append("model_generation/PatternFiles")
    sys.argv.append("--ofd")
    sys.argv.append("model_generation/CodeFiles")

    PCGen_new()
