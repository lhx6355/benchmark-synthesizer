import os
import sys
import shutil

## 删除 CodeFiles 以及 PatternFiles 文件夹下所有未被使用的文件
## 根据 CodeFiles 下的文件大小是否为0进行判断

BASE_DIR    = os.path.dirname(__file__)
CPATH_DIR   = BASE_DIR + '\\CodeFiles'
CPATH_DIR2  = BASE_DIR + '\\CodeFiles2'

TRACE_DIR   = BASE_DIR + '\\ModelTrace'
PATTERN_DIR = BASE_DIR + '\\PatternFiles'


def remove_TraceFiles():
    trace_file = []
    cpath_file = []
    pattern_file = []

    last_trace_name = 'instrace.85-sta.00496.0000.log.txt'

# 根据 CodeFiles 删除 PatternFiles 文件夹下所有未被使用的文件
    for root, dirs, files in os.walk(CPATH_DIR): 
        for file in files:
            cpath_file.append(file.split('.')[0])

    for root, dirs, files in os.walk(PATTERN_DIR): 
        for file in files:
            pattern_file = file.split('.')[0]
            if pattern_file in cpath_file:
                pass
            else:
                os.remove(os.path.join(PATTERN_DIR, file))


# 根据制定规则，删除不满足

    # for root, dirs, files in os.walk(TRACE_DIR): 
    #     for file in files:
    #         trace_file.append(file.split('.')[1].split('-')[0])


    # for root, dirs, files in os.walk(CPATH_DIR): 
    #     for file in files:
    #         # cpath_file.append(file.split('.')[0])
    #         cpath_name = file.split('.')[0]
    #         if cpath_name in trace_file:
    #             shutil.move(os.path.join(CPATH_DIR, file), CPATH_DIR2)
    #         # if last_trace_name.split('.')[1].split('-')[0] == file.split('.')[1].split('-')[0]:
    #         #     trace_time1 = os.path.getmtime(os.path.join(TRACE_DIR, last_trace_name))
    #         #     trace_time2 = os.path.getmtime(os.path.join(TRACE_DIR, file))
    #         #     if trace_time1 > trace_time2:
    #         #         os.remove(os.path.join(TRACE_DIR, last_trace_name))
    #         #     else:
    #         #         os.remove(os.path.join(TRACE_DIR, file))
    #         #     print(trace_name + '\n')
    #         # last_trace_name = file



# def remove_TraceFiles():
#     for root, dirs, files in os.walk(CPATH_DIR): 


if __name__ == '__main__':
    remove_TraceFiles()
