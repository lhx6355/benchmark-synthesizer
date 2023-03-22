# ------
# Author:
# Email:  lycheenice@gmail.com
# Create: 2016-09-26 by lychee
# Modify: 2016-09-27
# Filename: PCGenUtils.py
#
# Description: convenient Utilities for Pattern Code Generator
# ------

import sys
import os
import getopt
import re
import json


def usage():
    print ('''
        Usage: python PCGen.py --if = InputPatternFile --of = OutputCodeFile
            --if  = InputFile
            --of  = OutputFile
            --ifd = InputDir
            --ofd = OutputDir
            -h | --help     : user manual, for details refer to README.md
        ''')

def commandline_parser():
    gv = { 'pattern_files': [],   # Input pattern parameters files list    
              'code_files': [],   # Output code file list                   --of
           'process_loops':  0,   # loops = length of input files list
                    'ppls': [] }  # Pattern Parameters ListS
    try:
        opts, args = getopt.getopt(sys.argv[1: ], "h", ["help", "if=", "ifd=", "of=", "ofd="])             # --if 只输入一个文件  --ifd 扫面目录下的所有json输入文件
    except getopt.GetoptError:
        print ('Error:')
        usage()
        sys.exit()

    output_dir = ''
    for pname, pvalue in opts: # Parser Part 1
        if pname in ('--of'):
            # Set output file name
            gv['code_files'].append(pvalue)
        elif pname in ('--ofd'):
            # Set output dir
            output_dir = pvalue
            if not os.path.exists(pvalue):
                os.mkdir(pvalue)


    for pname, pvalue in opts: # Parser Part 2
        if pname in ('--if'):
            # Set input file name
            gv['pattern_files'].append(pvalue)
            # Set process loop to 1
            gv['process_loops'] = 1
        elif pname in ('--ifd'):
            for root, dirs, files in os.walk(pvalue):       # root 表示当前正在访问的文件夹路径 dirs 表示该文件夹下的子目录名list  files 表示该文件夹下的文件list
                if pvalue in root:
                    for f in files:
                        if re.match('.*json', f):           # 如果 f 是json文件
                            # Set input files name
                            gv['pattern_files'].append(pvalue + '/' + f)
                            # Set output files name
                            gv['code_files'].append(output_dir + '/' + f.replace('.json','') + '.c')    # 每一个json文件都生成一个对应的 c 文件
                            # Set process loops
                            gv['process_loops'] = len(gv['pattern_files'])                              # json输入文件的个数
            if gv['process_loops'] == 0:
                usage()
                sys.exit(-1)

    if gv['process_loops'] == 0:
        usage()
        sys.exit(-1)
    return gv

def patterninput_parser(gv):
    for i, pattern_file in enumerate(gv['pattern_files']):      # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
        gv['ppls'].append(json.load(open(pattern_file)))        # 读入json文件的内容

