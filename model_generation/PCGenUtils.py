import sys
import os
import getopt
import re
import json
import shutil


def usage():
    print ('''
            Usage: python PCGen.py
                --ifd = InputDir
                --ofd = OutputDir
        ''')

def commandline_parser():
    gv = { 'pattern_files': [],   # Input pattern parameters files list    
              'code_files': [],   # Output code file list
           'process_loops':  0,   # loops = length of input files list
                    'ppls': [] }  # Pattern Parameters ListS
    try:
        opts, args = getopt.getopt(sys.argv[1: ], "h", ["help", "ifd=", "ofd="])                    #  --ifd 扫面目录下的所有json输入文件
    except getopt.GetoptError:
        print ('Error:')
        usage()
        sys.exit()

    BASE_DIR = os.path.dirname(__file__)
    for pname, pvalue in opts:      # Parser Part 1
        if pname in ('--ofd'):
            output_dir = pvalue
            if os.path.exists(os.path.join(BASE_DIR, output_dir)):
                shutil.rmtree(os.path.join(BASE_DIR, output_dir))                                   # 递归删除文件夹下的所有子文件夹和子文件
            os.mkdir(os.path.join(BASE_DIR, output_dir))

    for pname, pvalue in opts:      # Parser Part 2
        if pname in ('--ifd'):
            for root, dirs, files in os.walk(os.path.join(BASE_DIR, pvalue)):                       # root 表示当前正在访问的文件夹路径 dirs 表示该文件夹下的子目录名list  files 表示该文件夹下的文件list
                for f in files:
                    if re.match('.*json', f):                                                       # 如果 f 是json文件
                        gv['pattern_files'].append(os.path.join(pvalue, f))
                        gv['code_files'].append(os.path.join(output_dir, f.replace('json', 'c')))   # 每一个json文件都生成一个对应的 c 文件
                        # open()必须使用绝对路径，不是很懂为什么
                        gv['ppls'].append(json.load(open(os.path.join(BASE_DIR, gv['pattern_files'][-1]))))
            # Set process loops
            gv['process_loops'] = len(gv['pattern_files'])                                          # json输入文件的个数

    if gv['process_loops'] == 0:
        usage()
        sys.exit(-1)

    return gv
