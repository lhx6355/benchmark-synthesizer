import json
import os
import sys
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
PATTERN_FILE_DIR = BASE_DIR + '\\PatternFiles-666'

# 这两行代码解决 plt 中文显示的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    pattern_list = []
    for root, dirs, files in os.walk(PATTERN_FILE_DIR, topdown=False):
        for file_name in files:
            pattern_file = PATTERN_FILE_DIR + '\\' + file_name
            pattern_list.append(json.load(open(pattern_file))) 


    # Inst_mix = [0] * 14
    CriticalPathLength = [0] * 41
    RegDependenceLength = [0] * 30
    LoadGlobalTemporal = [0] * 12
    StoreGlobalTemporal = [0] * 12
    LoadGlobalSpatial = [0] * 12
    StoreGlobalSpatial = [0] * 12
    InstFetchReuseDist = [0] * 11
    InstFetchAddrDist = [0] * 11

    for i in range(len(pattern_list)):
        CriticalPathLength[pattern_list[i]['ILP']['CriticalPathLength']] = CriticalPathLength[pattern_list[i]['ILP']['CriticalPathLength']] + 1
        RegDependenceLength[pattern_list[i]['ILP']['RegDependenceLength']] = RegDependenceLength[pattern_list[i]['ILP']['RegDependenceLength']] + 1

        LoadGlobalTemporal[pattern_list[i]['Locality']['LoadGlobalTemporal']] = LoadGlobalTemporal[pattern_list[i]['Locality']['LoadGlobalTemporal']] + 1
        StoreGlobalTemporal[pattern_list[i]['Locality']['StoreGlobalTemporal']] = StoreGlobalTemporal[pattern_list[i]['Locality']['StoreGlobalTemporal']] + 1
        LoadGlobalSpatial[pattern_list[i]['Locality']['LoadGlobalSpatial']] = LoadGlobalSpatial[pattern_list[i]['Locality']['LoadGlobalSpatial']] + 1
        StoreGlobalSpatial[pattern_list[i]['Locality']['StoreGlobalSpatial']] = StoreGlobalSpatial[pattern_list[i]['Locality']['StoreGlobalSpatial']] + 1

        InstFetchReuseDist[pattern_list[i]['Locality']['InstFetchReuseDist']] = InstFetchReuseDist[pattern_list[i]['Locality']['InstFetchReuseDist']] + 1
        InstFetchAddrDist[pattern_list[i]['Locality']['InstFetchAddrDist']] = InstFetchAddrDist[pattern_list[i]['Locality']['InstFetchAddrDist']] + 1

    
    plt.figure()
    plt.bar(range(len(CriticalPathLength)), CriticalPathLength)
    plt.title('关键路径长度分布统计')

    plt.figure()
    plt.bar(range(len(RegDependenceLength)), RegDependenceLength)
    plt.title('寄存器依赖距离分布统计')

    plt.figure()
    plt.bar(range(len(LoadGlobalTemporal)), LoadGlobalTemporal)
    plt.title('LoadGlobalTemporal分布统计')

    plt.figure()
    plt.bar(range(len(StoreGlobalTemporal)), StoreGlobalTemporal)
    plt.title('StoreGlobalTemporal分布统计')

    plt.figure()
    plt.bar(range(len(LoadGlobalSpatial)), LoadGlobalSpatial)
    plt.title('LoadGlobalSpatial分布统计')


    plt.figure()
    plt.bar(range(len(StoreGlobalSpatial)), StoreGlobalSpatial)
    plt.title('StoreGlobalSpatial分布统计')

    plt.figure()
    plt.bar(range(len(InstFetchReuseDist)), InstFetchReuseDist)
    plt.title('InstFetchReuseDist分布统计')

    plt.figure()
    plt.bar(range(len(InstFetchAddrDist)), InstFetchAddrDist)
    plt.title('InstFetchAddrDist分布统计')        

    plt.show()

if __name__ == '__main__':
    main()
