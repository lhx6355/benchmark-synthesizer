import os
import pickle
import shutil

def benchmark_sythesizer(filepath):
	BASE_DIR = os.path.dirname(__file__)
	benchmarks_path 	= os.path.join(filepath, 'Benchmark')
	model_file_path 	= os.path.join(BASE_DIR, '..\\template_files\\CodeFiles')					# 改为--ofd的值 ？

	model_selected_file = open(os.path.join(filepath, 'Select\\model_selected.pkl'), 					'rb')
	model_name_file 	= open(os.path.join(BASE_DIR, '..\\template_files\\ModelMat\\modelName.pkl'), 	'rb')
	workload_name_file 	= open(os.path.join(filepath, 'MICA\\workloadName.pkl'), 						'rb')
	weight_file 		= open(os.path.join(filepath, 'Cluster\\selected_weight.pkl'), 					'rb')

	model_selecteds 	= pickle.load(model_selected_file)
	model_names 		= pickle.load(model_name_file)
	workload_names 		= pickle.load(workload_name_file)
	weight 				= pickle.load(weight_file)

	# weight_cal = [0] * len(weight)
	# model_num = int(5000000 / 100000)																		# 期望的bench指令数 / 一个model的指令数
	# weight_sum = sum(weight)

	# max_weight = max(weight)																				#  权重相关
	# for i in range(len(weight)):
	# 	weight_cal[i] = int(model_num * (weight[i] / weight_sum)) + 1
	# weight = weight_cal

	# # min_weight = min(weight)
	# # for i in range(len(weight)):
	# # 	if weight[i] < max_weight + 1:
	# # 		weight[i] = int(weight[i] / min_weight)
	# # 	else:
	# # 		weight[i] = 1

	benchmark_path = os.path.join(benchmarks_path, 'bench_' + workload_names[0] + '.c')						# 要合成的文件名字
	benchmark_file = open(benchmark_path, 'w+')
	benchmark_file.write("int temp[5000000][200] = {0};\n")
	benchmark_file.write("void *ptr = temp + 500000 / 2;\n")

	temp = benchmark_path.split('.')
	benchmark_use_file_path = temp[0]

	if os.path.exists(benchmark_use_file_path):
		shutil.rmtree(benchmark_use_file_path)
	os.mkdir(benchmark_use_file_path)

	log_file = open(benchmark_use_file_path + "\\log.txt", 'w+')

	functions = []

	# model_selecteds = [[1 for i in range(100)]]
	for k in range(0, len(model_selecteds)):			# 33 * 25933 ？？？
		print ('synthesizing benchmark for workload cluster ' + str(k))
		log_file.writelines('synthesizing benchmark for workload cluster ' + str(k) +  ':  ' + str(weight[k]) + '\n')
		if weight[k] == 0 :																		# weight为0时，放弃合成该interval
			continue
		cluster_func = []
		cluster_file = open(benchmark_use_file_path + "\\cluster" + str(k) + '.c', 'w+')
		cluster_file.write("int temp[5000000] = {1};\n")
		cluster_file.write("void *ptr = temp + 500000 / 2;\n")

		model_selected = model_selecteds[k]
		for i in range(0, len(model_selected)):													# model的数量 25933
			if model_selected[i] == 0 :
				continue
			else:
				model_CFileName = model_names[i].split('.')[1]
				model_CFileName = model_CFileName.split('-')[0]

				print(os.path.join(model_file_path, model_CFileName + '.c'))
				log_file.writelines(os.path.join(model_file_path, model_CFileName + '.c' + '\n'))

				func_callCmd = "\tfunc" + model_CFileName + "();\n"

				cluster_func.append(func_callCmd)														# cluster begin
				model_file = open(os.path.join(model_file_path, model_CFileName + '.c'), 'r+')

				lines = model_file.readlines()
				for line in range(0, len(lines)):
					if "int temp[5000000] = {1};" in lines[line]:
						continue
					if "main()" not in lines[line]:
						if "#0x500000" in lines[line]:													# 替换原本的访存地址
							# lines[line] = lines[line].replace('#0x500000', 'x11')
							lines[line] = lines[line].replace('#0x500000', '#0x15d0000')
						cluster_file.write(lines[line])
					else:
						break																			# cluster begin


				if(func_callCmd in functions):
					for j in range(0, int(weight[k])):
						functions.append(func_callCmd)
					continue
				else:
					for j in range(0, int(weight[k])):
						functions.append(func_callCmd)

				model_file = open(os.path.join(model_file_path, model_CFileName + '.c'), 'r+')

				lines = model_file.readlines()
				for line in range(0, len(lines)):
					if "int temp[5000000] = {1};" in lines[line]:
						continue
					if "main()" not in lines[line]:
						if "#0x500000" in lines[line]:
							# lines[line] = lines[line].replace('#0x500000', 'x11')
							lines[line] = lines[line].replace('#0x500000', '#0x15d0000')
						benchmark_file.write(lines[line])
					else:
						break
			
		cluster_file.writelines("int main(){\n")
		cluster_file.writelines(' asm volatile ("ldr x11, %0; ": "+m" (ptr) :: "x11"); \n')
		for j in range(0, len(cluster_func)):
			cluster_file.writelines("\t" + cluster_func[j])
		cluster_file.writelines("\n\treturn 0;\n}")
		cluster_file.close()
				# shutil.copyfile(os.path.join(model_file_path, model_CFileName + '.c'), os.path.join(benchmark_use_file_path, model_CFileName + '.c'))
		
	benchmark_file.writelines("int main(){\n")						# 开始写主函数的内容
	benchmark_file.writelines(' asm volatile ("ldr x11, %0; ": "+m" (ptr) :: "x11"); \n')

	for j in range(0, len(functions)):
		benchmark_file.writelines("\t" + functions[j])

	benchmark_file.writelines("\n\treturn 0;\n}")
	benchmark_file.close()

	model_selected_file.close()
	model_name_file.close()
	workload_name_file.close()

	log_file.close()

if __name__ == '__main__':
	filepath = 'D:\\Project\\OPPO\\benchmark-synthesizer-function\\workload_files\\one-hundred'
	benchmark_sythesizer(filepath)