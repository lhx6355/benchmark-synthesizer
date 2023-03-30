# -*- coding: UTF-8 -*-
import os
import random
import json
import math
import shutil

"""generate parameters in form of dict

generate 25 parameters into json file as input for code generation phase;
25 parameters are:
	11 for instruction mix: SIMD, load, store, int alu, int multi div, int mul, fp neon alu, fp neon div, fp  neon mul, branch 
	2 for instruction locality: fetch reuse distance, fetch address distance
	8 for data locality: load/store global/local temporal/spatial length
	2 for ILP:
	1 for branch:
	and serial block size
Returns:
	dict -- dict with 25 parameters as input of function print_json
"""

def gen_json():
# domain of each parameter
	# instruction mix
	SIMD_NUM_MIN = 0  
	SIMD_NUM_MAX = 100000
	LOAD_INST_NUM_MIN = 0
	LOAD_INST_NUM_MAX = 100000
	STORE_INST_NUM_MIN = 0
	STORE_INST_NUM_MAX = 100000
	SERIAL_INST_NUM_MIN = 0
	SERIAL_INST_NUM_MAX = 100000
	INT_ALU_INST_NUM_MIN = 0
	INT_ALU_INST_NUM_MAX = 100000
	INT_MULTI_DIV_NUM_MIN = 0
	INT_MULTI_DIV_NUM_MAX = 100000
	INT_MUL_NUM_MIN = 0
	INT_MUL_NUM_MAX = 100000
	FP_NEON_ALU_NUM_MIN = 0
	FP_NEON_ALU_NUM_MAX = 100000
	FP_NEON_DIV_NUM_MIN = 0
	FP_NEON_DIV_NUM_MAX = 100000
	FP_NEON_MUL_NUM_MIN = 0
	FP_NEON_MUL_NUM_MAX = 100000
	BRANCH_INST_NUM_MIN = 0
	BRANCH_INST_NUM_MAX = 100000

	# ILP
	CRITICAL_PATH_LENGTH_MIN = 0
	CRITICAL_PATH_LENGTH_MAX = 40
	REG_DEPENDENCE_LENGTH_MIN = 0
	REG_DEPENDENCE_LENGTH_MAX = 29

	# locality
	INST_FETCH_REUSE_DIST_MIN = 0
	INST_FETCH_REUSE_DIST_MAX = 9
	INST_FETCH_ADDR_DIST_MIN = 0
	INST_FETCH_ADDR_DIST_MAX = 9

	LOAD_LOCAL_SPATIAL_MIN = 0
	LOAD_LOCAL_SPATIAL_MAX = 11
	LOAD_GLOBAL_SPATIAL_MIN = 0
	LOAD_GLOBAL_SPATIAL_MAX = 11
	LOAD_LOCAL_TEMPORAL_MIN = 0
	LOAD_LOCAL_TEMPORAL_MAX = 11
	LOAD_GLOBAL_TEMPORAL_MIN = 0
	LOAD_GLOBAL_TEMPORAL_MAX = 11
	STORE_LOCAL_SPATIAL_MIN = 0
	STORE_LOCAL_SPATIAL_MAX = 11
	STORE_GLOBAL_SPATIAL_MIN = 0
	STORE_GLOBAL_SPATIAL_MAX = 11
	STORE_LOCAL_TEMPORAL_MIN = 0
	STORE_LOCAL_TEMPORAL_MAX = 11
	STORE_GLOBAL_TEMPORAL_MIN = 0
	STORE_GLOBAL_TEMPORAL_MAX = 11

	# Others
	BRANCH_TRANSITION_RATE_MIN = 0.0
	BRANCH_TRANSITION_RATE_MAX = 1.0
	SERIAL_BLOCK_SIZE_MIN = 1
	SERIAL_BLOCK_SIZE_MAX = 14

# initialize a parameter dict, each parameter to 0
	para_dict = {
				'InstMix': {
							'SIMDNum': 0,
							'LoadInstNum': 0,    
							'StoreInstNum': 0,    
							'SerialInstNum': 0,        
							'IntAluInstNum': 0,    
							'IntMultiDivNum': 0,    
							'IntMulNum': 0,    
							'FpNeonAluNum': 0,    
							'FpNeonDivNum': 0,    
							'FpNeonMulNum': 0,
							'BranchInstNum':0
							},
				'Locality': {
							'InstFetchReuseDist': 0,
							'InstFetchAddrDist': 0,
							'LoadLocalSpatial': 0,
							'LoadGlobalSpatial': 0,
							'LoadLocalTemporal': 0,
							'LoadGlobalTemporal': 0,
							'StoreLocalSpatial': 0,
							'StoreGlobalSpatial': 0,
							'StoreLocalTemporal': 0,
							'StoreGlobalTemporal': 0
							},
				'ILP':       {
							'CriticalPathLength': 0,
							'RegDependenceLength': 0
							},
							'BranchTransitionRate': 0.0,
							'SerialBlockSize': 0
				}

# set each parameter
# instruction mix -- method1
	SIMDNum = \
		random.randint(1, 1000)	
		# random.randint(SIMD_NUM_MIN, SIMD_NUM_MAX) 
	para_dict['InstMix']['SIMDNum'] = SIMDNum

	LoadInstNum = \
		random.randint(1, 2000)
		#random.randint(LOAD_INST_NUM_MIN, LOAD_INST_NUM_MAX)
	para_dict['InstMix']['LoadInstNum'] = LoadInstNum
	StoreInstNum = \
		random.randint(1, 2000)
		#random.randint(STORE_INST_NUM_MIN, STORE_INST_NUM_MAX)
	para_dict['InstMix']['StoreInstNum'] = StoreInstNum

	SerialInstNum = \
		random.randint(1, 30)
		#random.randint(SERIAL_INST_NUM_MIN, SERIAL_INST_NUM_MAX)
	para_dict['InstMix']['SerialInstNum'] = SerialInstNum

	IntAluInstNum = \
		random.randint(3500, 9500)
		#random.randint(INT_ALU_INST_NUM_MIN, INT_ALU_INST_NUM_MAX)
	para_dict['InstMix']['IntAluInstNum'] = IntAluInstNum
	IntMultiDivNum = \
		random.randint(100, 1600)
		#random.randint(INT_MULTI_DIV_NUM_MIN, INT_MULTI_DIV_NUM_MAX)
	para_dict['InstMix']['IntMultiDivNum'] = IntMultiDivNum
	IntMulNum = \
		random.randint(1, 20)
		#random.randint(INT_MUL_NUM_MIN, INT_MUL_NUM_MAX)
	para_dict['InstMix']['IntMulNum'] = IntMulNum

	FpNeonAluNum = \
		random.randint(1, 30)
		#random.randint(FP_NEON_ALU_NUM_MIN, FP_NEON_ALU_NUM_MAX)		
	para_dict['InstMix']['FpNeonAluNum'] = FpNeonAluNum
	FpNeonDivNum = \
		random.randint(1, 20)
		#random.randint(FP_NEON_DIV_NUM_MIN, FP_NEON_DIV_NUM_MAX)
	para_dict['InstMix']['FpNeonDivNum'] = FpNeonDivNum
	FpNeonMulNum = \
		random.randint(1, 20)
		#random.randint(FP_NEON_MUL_NUM_MIN, FP_NEON_MUL_NUM_MAX)
	para_dict['InstMix']['FpNeonMulNum'] = FpNeonMulNum
	# branch inst num cannot be zero                                     25%
	BranchInstNum = \
		random.randint(0, 4000)
		#random.randint(BRANCH_INST_NUM_MIN, BRANCH_INST_NUM_MAX)
	para_dict['InstMix']['BranchInstNum'] = BranchInstNum

	#ILP
	CriticalPathLength = \
		random.randint(CRITICAL_PATH_LENGTH_MIN, CRITICAL_PATH_LENGTH_MAX)
	para_dict['ILP']['CriticalPathLength'] = CriticalPathLength
	RegDependenceLength = \
		random.randint(REG_DEPENDENCE_LENGTH_MIN, REG_DEPENDENCE_LENGTH_MAX)
	para_dict['ILP']['RegDependenceLength'] = RegDependenceLength

	#locality
	InstFetchReuseDist = \
		random.randint(INST_FETCH_REUSE_DIST_MIN, INST_FETCH_REUSE_DIST_MAX)
	para_dict['Locality']['InstFetchReuseDist'] = InstFetchReuseDist
	InstFetchAddrDist = \
		random.randint(INST_FETCH_ADDR_DIST_MIN, INST_FETCH_ADDR_DIST_MAX)
	para_dict['Locality']['InstFetchAddrDist'] = InstFetchAddrDist
	LoadLocalSpatial = \
		random.randint(LOAD_LOCAL_SPATIAL_MIN, LOAD_LOCAL_SPATIAL_MAX)
	para_dict['Locality']['LoadLocalSpatial'] = LoadLocalSpatial
	LoadGlobalSpatial = \
		random.randint(LOAD_GLOBAL_SPATIAL_MIN, LOAD_GLOBAL_SPATIAL_MAX)
	para_dict['Locality']['LoadGlobalSpatial'] = LoadGlobalSpatial
	LoadLocalTemporal = \
		random.randint(LOAD_LOCAL_TEMPORAL_MIN, LOAD_LOCAL_TEMPORAL_MAX)
	para_dict['Locality']['LoadLocalTemporal'] = LoadLocalTemporal
	LoadGlobalTemporal = \
		random.randint(LOAD_GLOBAL_TEMPORAL_MIN, LOAD_GLOBAL_TEMPORAL_MAX)
	para_dict['Locality']['LoadGlobalTemporal'] = LoadGlobalTemporal
	StoreLocalSpatial = \
		random.randint(STORE_LOCAL_SPATIAL_MIN, STORE_LOCAL_SPATIAL_MAX)
	para_dict['Locality']['StoreLocalSpatial'] = StoreLocalSpatial
	StoreGlobalSpatial = \
		random.randint(STORE_GLOBAL_SPATIAL_MIN, STORE_GLOBAL_SPATIAL_MAX)
	para_dict['Locality']['StoreGlobalSpatial'] = StoreGlobalSpatial
	StoreLocalTemporal = \
		random.randint(STORE_LOCAL_TEMPORAL_MIN, STORE_LOCAL_TEMPORAL_MAX)
	para_dict['Locality']['StoreLocalTemporal'] = StoreLocalTemporal
	StoreGlobalTemporal = \
		random.randint(STORE_GLOBAL_TEMPORAL_MIN, STORE_GLOBAL_TEMPORAL_MAX)
	para_dict['Locality']['StoreGlobalTemporal'] = StoreGlobalTemporal

	#others
	BranchTransitionRate = \
		random.random()
	para_dict['BranchTransitionRate'] = BranchTransitionRate
	SerialBlockSize = \
		random.randint(SERIAL_BLOCK_SIZE_MIN, SERIAL_BLOCK_SIZE_MAX)
	para_dict['SerialBlockSize'] = SerialBlockSize



	return para_dict

def gen_para(json_num, gen_type, *target_vector):
	SIMD_NUM_MIN = 0
	SIMD_NUM_MAX = 20000
	LOAD_INST_NUM_MIN = 0
	LOAD_INST_NUM_MAX = 20000
	STORE_INST_NUM_MIN = 0
	STORE_INST_NUM_MAX = 20000
	BRANCH_INST_NUM_MIN = 0
	BRANCH_INST_NUM_MAX = 20000
	SERIAL_INST_NUM_MIN = 0
	SERIAL_INST_NUM_MAX = 20000
	INT_ALU_INST_NUM_MIN = 0
	INT_ALU_INST_NUM_MAX = 20000
	INT_MULTI_DIV_NUM_MIN = 0
	INT_MULTI_DIV_NUM_MAX = 20000
	INT_MUL_NUM_MIN = 0
	INT_MUL_NUM_MAX = 20000
	FP_NEON_ALU_NUM_MIN = 0
	FP_NEON_ALU_NUM_MAX = 20000
	FP_NEON_DIV_NUM_MIN = 0
	FP_NEON_DIV_NUM_MAX = 20000
	FP_NEON_MUL_NUM_MIN = 0
	FP_NEON_MUL_NUM_MAX = 20000

	#locality
	INST_FETCH_REUSE_DIST_MIN = 0
	INST_FETCH_REUSE_DIST_MAX = 10 + 1				# + 1 ？
	INST_FETCH_ADDR_DIST_MIN = 0
	INST_FETCH_ADDR_DIST_MAX = 10 + 1
	LOAD_LOCAL_SPATIAL_MIN = 0
	LOAD_LOCAL_SPATIAL_MAX = 11 + 1
	LOAD_GLOBAL_SPATIAL_MIN = 0
	LOAD_GLOBAL_SPATIAL_MAX = 11 + 1
	LOAD_LOCAL_TEMPORAL_MIN = 0
	LOAD_LOCAL_TEMPORAL_MAX = 11 + 1
	LOAD_GLOBAL_TEMPORAL_MIN = 0
	LOAD_GLOBAL_TEMPORAL_MAX = 11 + 1
	STORE_LOCAL_SPATIAL_MIN = 0
	STORE_LOCAL_SPATIAL_MAX = 11 + 1
	STORE_GLOBAL_SPATIAL_MIN = 0
	STORE_GLOBAL_SPATIAL_MAX = 11 + 1
	STORE_LOCAL_TEMPORAL_MIN = 0
	STORE_LOCAL_TEMPORAL_MAX = 11 + 1
	STORE_GLOBAL_TEMPORAL_MIN = 0
	STORE_GLOBAL_TEMPORAL_MAX = 11 + 1
	#ILP
	CRITICAL_PATH_LENGTH_MIN = 0
	CRITICAL_PATH_LENGTH_MAX = 40 + 1
	REG_DEPENDENCE_LENGTH_MIN = 0
	REG_DEPENDENCE_LENGTH_MAX = 29 + 1
	#Others
	BRANCH_TRANSITION_RATE_MIN = 0.0
	BRANCH_TRANSITION_RATE_MAX = 1.0
	SERIAL_BLOCK_SIZE_MIN = 1
	SERIAL_BLOCK_SIZE_MAX = 14 + 1

#initialize a parameter dict, each parameter to 0
	para_dict = {
				    'InstMix': {
        					   	   'SIMDNum': 0,
                                   'LoadInstNum': 0,    
        							'StoreInstNum': 0,    
        							'SerialInstNum': 0,        
        							'IntAluInstNum': 0,    
        							'IntMultiDivNum': 0,    
							        'IntMulNum': 0,    
							        'FpNeonAluNum': 0,    
							        'FpNeonDivNum': 0,    
							        'FpNeonMulNum': 0,
							        'BranchInstNum':0
    							},
    				'Locality': {
							        'InstFetchReuseDist': 0,
							        'InstFetchAddrDist': 0,
							        'LoadLocalSpatial': 0,
							        'LoadGlobalSpatial': 0,
							        'LoadLocalTemporal': 0,
							        'LoadGlobalTemporal': 0,
							        'StoreLocalSpatial': 0,
							        'StoreGlobalSpatial': 0,
							        'StoreLocalTemporal': 0,
							        'StoreGlobalTemporal': 0
    							},
 				   'ILP':       {
							        'CriticalPathLength': 0,
        							'RegDependenceLength': 0
    							},
    								'BranchTransitionRate': 0.0,
    								'SerialBlockSize': 0
				}	

	# random seed
	angle_array_1 = []
	for i in range(10):
		angle_array_1.append(math.pi * random.random() / 2) # random.random()  [0, 1) 范围内生成随机数
	seed_array_1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	# seed[0] = math.sin(angle_array_1[0])
	for i in range(10):
		for j in range(0, i):
			seed_array_1[i] *= math.cos(angle_array_1[j])
		if i == 9:
			seed_array_1[10] =  seed_array_1[i] * math.cos(angle_array_1[i])
		seed_array_1[i] *= math.sin(angle_array_1[i])

	# print 'seed_array_1 is: '
	# print seed_array_1

	if gen_type == 1:
		SIMDNum = \
			int(SIMD_NUM_MAX * seed_array_1[0])
		para_dict['InstMix']['SIMDNum'] = SIMDNum
		LoadInstNum = \
			int(LOAD_INST_NUM_MAX * seed_array_1[1])
		para_dict['InstMix']['LoadInstNum'] = LoadInstNum
		StoreInstNum = \
			int(STORE_INST_NUM_MAX * seed_array_1[2])
		para_dict['InstMix']['StoreInstNum'] = StoreInstNum
		SerialInstNum = \
			int(SERIAL_INST_NUM_MAX * seed_array_1[3])
		para_dict['InstMix']['SerialInstNum'] = SerialInstNum
		IntAluInstNum = \
			int(INT_ALU_INST_NUM_MAX * seed_array_1[4])				
		para_dict['InstMix']['IntAluInstNum'] = IntAluInstNum + LoadInstNum + StoreInstNum		# lhx
		IntMultiDivNum = \
			int(INT_MULTI_DIV_NUM_MAX * seed_array_1[5])
		para_dict['InstMix']['IntMultiDivNum'] = IntMultiDivNum
		IntMulNum = \
			int(INT_MUL_NUM_MAX * seed_array_1[6])
		para_dict['InstMix']['IntMulNum'] = IntMulNum
		FpNeonAluNum = \
			int(FP_NEON_ALU_NUM_MAX * seed_array_1[7])	
		para_dict['InstMix']['FpNeonAluNum'] = FpNeonAluNum
		FpNeonDivNum = \
			int(FP_NEON_DIV_NUM_MAX * seed_array_1[8])
		para_dict['InstMix']['FpNeonDivNum'] = FpNeonDivNum
		FpNeonMulNum = \
			int(FP_NEON_MUL_NUM_MAX * seed_array_1[9])
		para_dict['InstMix']['FpNeonMulNum'] = FpNeonMulNum
		# branch inst num cannot be zero
		BranchInstNum = \
			int(BRANCH_INST_NUM_MAX * seed_array_1[10])
		para_dict['InstMix']['BranchInstNum'] = BranchInstNum
		
		angle_array_2 = []
		for i in range(9):
			angle_array_2.append(math.pi * random.random() / 2)
		seed_array_2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
		# seed[0] = math.sin(angle_array_2[0])
		for i in range(9):
			for j in range(0, i):
				seed_array_2[i] *= math.cos(angle_array_2[j])
			if i == 8:
				seed_array_2[9] = seed_array_2[i] * math.cos(angle_array_2[i])
			seed_array_2[i] *= math.sin(angle_array_2[i])
		# print 'seed_array_2 is: '
		# print seed_array_2

		# locality
		InstFetchReuseDist = \
			int(INST_FETCH_REUSE_DIST_MAX * seed_array_2[0])
			# random.randint(INST_FETCH_REUSE_DIST_MIN, INST_FETCH_REUSE_DIST_MAX)
		para_dict['Locality']['InstFetchReuseDist'] = InstFetchReuseDist
		InstFetchAddrDist = \
			int(INST_FETCH_ADDR_DIST_MAX * seed_array_2[1])
			# random.randint(INST_FETCH_ADDR_DIST_MIN, INST_FETCH_ADDR_DIST_MAX)
		para_dict['Locality']['InstFetchAddrDist'] = InstFetchAddrDist
		LoadLocalSpatial = \
			int(LOAD_LOCAL_SPATIAL_MAX * seed_array_2[2])
			# random.randint(LOAD_LOCAL_SPATIAL_MIN, LOAD_LOCAL_SPATIAL_MAX)
		para_dict['Locality']['LoadLocalSpatial'] = LoadLocalSpatial
		LoadGlobalSpatial = \
			int(LOAD_GLOBAL_SPATIAL_MAX * seed_array_2[3])
			# random.randint(LOAD_GLOBAL_SPATIAL_MIN, LOAD_GLOBAL_SPATIAL_MAX)
		para_dict['Locality']['LoadGlobalSpatial'] = LoadGlobalSpatial
		LoadLocalTemporal = \
			int(LOAD_LOCAL_TEMPORAL_MAX * seed_array_2[4])
			# random.randint(LOAD_LOCAL_TEMPORAL_MIN, LOAD_LOCAL_TEMPORAL_MAX)
		para_dict['Locality']['LoadLocalTemporal'] = LoadLocalTemporal
		LoadGlobalTemporal = \
			int(LOAD_GLOBAL_TEMPORAL_MAX * seed_array_2[5])
			# random.randint(LOAD_GLOBAL_TEMPORAL_MIN, LOAD_GLOBAL_TEMPORAL_MAX)
		para_dict['Locality']['LoadGlobalTemporal'] = LoadGlobalTemporal
		StoreLocalSpatial = \
			int(STORE_LOCAL_SPATIAL_MAX * seed_array_2[6])
			# random.randint(STORE_LOCAL_SPATIAL_MIN, STORE_LOCAL_SPATIAL_MAX)
		para_dict['Locality']['StoreLocalSpatial'] = StoreLocalSpatial
		StoreGlobalSpatial = \
			int(STORE_GLOBAL_SPATIAL_MAX * seed_array_2[7])
			# random.randint(STORE_GLOBAL_SPATIAL_MIN, STORE_GLOBAL_SPATIAL_MAX)
		para_dict['Locality']['StoreGlobalSpatial'] = StoreGlobalSpatial
		StoreLocalTemporal = \
			int(STORE_LOCAL_TEMPORAL_MAX * seed_array_2[8])
			# random.randint(STORE_LOCAL_TEMPORAL_MIN, STORE_LOCAL_TEMPORAL_MAX)
		para_dict['Locality']['StoreLocalTemporal'] = StoreLocalTemporal
		StoreGlobalTemporal = \
			int(STORE_GLOBAL_TEMPORAL_MAX * seed_array_2[9])
			# random.randint(STORE_GLOBAL_TEMPORAL_MIN, STORE_GLOBAL_TEMPORAL_MAX)
		para_dict['Locality']['StoreGlobalTemporal'] = StoreGlobalTemporal

		angle_array_3 = []
		for i in range(3):
			angle_array_3.append(math.pi * random.random() / 2)
		seed_array_3 = [1, 1, 1, 1]
		# seed[0] = math.sin(angle_array_3[0])
		for i in range(3):
			for j in range(0, i):
				seed_array_3[i] *= math.cos(angle_array_3[j])
			if i == 2:
				seed_array_3[3] = seed_array_3[i] * math.cos(angle_array_3[i])
			seed_array_3[i] *= math.sin(angle_array_3[i])
		# print 'seed_array_3 is: '
		# print seed_array_3

		# ILP
		CriticalPathLength = \
			int(CRITICAL_PATH_LENGTH_MAX * seed_array_3[0])
			# random.randint(CRITICAL_PATH_LENGTH_MIN, CRITICAL_PATH_LENGTH_MAX)
		para_dict['ILP']['CriticalPathLength'] = CriticalPathLength
		RegDependenceLength = \
			int(REG_DEPENDENCE_LENGTH_MAX * seed_array_3[1])
			# random.randint(REG_DEPENDENCE_LENGTH_MIN, REG_DEPENDENCE_LENGTH_MAX)
		para_dict['ILP']['RegDependenceLength'] = RegDependenceLength
		# others
		BranchTransitionRate = \
			BRANCH_TRANSITION_RATE_MAX * seed_array_3[2]
			# random.random()
		para_dict['BranchTransitionRate'] = BranchTransitionRate
		SerialBlockSize = \
			int(math.ceil(SERIAL_BLOCK_SIZE_MAX * seed_array_3[3]))
			# random.randint(SERIAL_BLOCK_SIZE_MIN, SERIAL_BLOCK_SIZE_MAX)
		para_dict['SerialBlockSize'] = SerialBlockSize

	elif gen_type == 2:
		# todo
		pass
	elif gen_type == 3:
		# todo
		pass
	elif gen_type == 4:
		# todo
		pass
	elif gen_type == 5:
		# todo
		pass
	
	return para_dict

def print_json(patternPath, para_dict, filename):
	"""print json file from the parameter dict
	Arguments:
		para_dict {dict} -- dict of input parameters
		filename {string} -- json file name, with suffix '.json'
	"""
	BASE_DIR = os.path.dirname(__file__)
	dest_file = os.path.join(BASE_DIR, patternPath ,filename)
	file = open(dest_file, 'w')
	json_obj = json.dumps(para_dict)
	file.write(json_obj)
	file.close()

def json_gen(PatternPath_path):
	# delete old files
	BASE_DIR = os.path.dirname(__file__)
	dest_dir = os.path.join(BASE_DIR, PatternPath_path)
	if os.path.exists(dest_dir):						# 如果之前旧的文件夹存在，则删除旧文件夹
		shutil.rmtree(dest_dir)							
	os.mkdir(dest_dir)									# 在当前目录下创建 PatternFiles 文件夹
	for i in range(100000, 200000):
	# for i in range(0, 10000):
		print (i)
		# para_dict = gen_para(json_num, 1)				# 一定规律的生成
		para_dict = gen_json()							# 随机的生成参数
		print_json(PatternPath_path, para_dict, str(i) + '.json')			# json写入文件

if __name__ == '__main__':
	json_gen('PatternFiles')