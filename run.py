import os
import pickle
import matlab.engine
import pickle
import sys

from model_generation import json_gen
from model_generation import PCGen_new
from model_selection  import benchmark_sythesizer

def model_gen():
	json_gen.json_gen('PatternFiles')

	sys.argv.append('--ifd')
	sys.argv.append('PatternFiles')
	sys.argv.append('--ofd')
	sys.argv.append('CodeFiles')
	PCGen_new.PCGen_new()

def fastmodel_workload(profilerType, filepath):
	print ('start function fastmodel_workload')
	eng = matlab.engine.start_matlab()
	eng.addpath(os.path.join(os.path.dirname(__file__), 'fastmodel_workload'), nargout = 0)
	[matrix_mat, name] = eng.txt2mat(profilerType, filepath, nargout = 2)
	eng.quit()

	if profilerType == "model":
		matrix_file = open('template_files\ModelMat\\modelMatrix.pkl', 'wb')
		name_file 	= open('template_files\ModelMat\\modelName.pkl', 'wb')
	else:
		matrix_file = open(os.path.join(filepath, 'MICA') +  '\workloadMatrix.pkl', 'wb')
		name_file 	= open(os.path.join(filepath, 'MICA') +  '\workloadName.pkl', 'wb')


	matrix = []
	for i in range(len(matrix_mat)):
		matrix.append([])
		for j in range(len(matrix_mat[0])):
			matrix[i].append(int(matrix_mat[i][j]))
	pickle.dump(matrix, matrix_file)
	pickle.dump(name, name_file)
	matrix_file.close()
	name_file.close()
	print ('end function fastmodel_workload -- ' + profilerType)

def clustering(filepath):
	print ('start function clustering')
	eng = matlab.engine.start_matlab()
	eng.addpath(os.path.join(os.path.dirname(__file__), 'clustering'), nargout = 0)
	eng.addpath(os.path.join(os.path.dirname(__file__), 'error_computation'), nargout = 0)
	[workload_matrix_selected, index_selected, class_selected_weight] = eng.cluster(filepath, nargout = 3)
	eng.quit()

	# convert matlab format into python list format       生成pkl格式文件，保存matlab数据
	selected_weight = []
	if type(class_selected_weight) is float:
		selected_weight.append(1)
	else:
		for i in range(len(class_selected_weight)):
			for j in range(len(class_selected_weight[0])):
				selected_weight.append(int(class_selected_weight[i][j]))
	file = open(os.path.join(filepath, 'Cluster') + '\selected_weight.pkl', 'wb')
	pickle.dump(selected_weight, file)
	file.close()
	print ('end function fastmodel_workload')

def model_selection(filepath):
	print ('start function model_selection')
	eng = matlab.engine.start_matlab()
	eng.addpath(os.path.join(os.path.dirname(__file__), 'model_selection'), nargout=0)
	eng.addpath(os.path.join(os.path.dirname(__file__), 'clustering'), nargout=0)
	eng.addpath(os.path.join(os.path.dirname(__file__), 'error_computation'), nargout=0)

	#3. model selection with genetic alogrithm with euclidean error in kmeans
	model_selected_mat = eng.model_select_genetic_eu(filepath, nargout = 1)
	eng.quit()

	# convert matlab format into python list format       生成pkl格式文件，保存matlab数据
	model_selected = []
	for i in range(len(model_selected_mat)):
		model_selected.append([])
		for j in range(len(model_selected_mat[0])):
			model_selected[i].append(int(model_selected_mat[i][j]))

	file = open(os.path.join(filepath, 'Select') + '\model_selected.pkl', 'wb')
	model_selected_file = pickle.dump(model_selected, file)
	file.close()
	print ('end function model_selection')

def error_computation():
	print ('start function error_computation')
	BASE_DIR = os.path.dirname(__file__)
	path_error_computation = os.path.join(BASE_DIR, 'error_computation')

	eng = matlab.engine.start_matlab('-nodesktop')
	eng.addpath(path_error_computation, nargout = 0)
	eng.run1(nargout = 0)																			# run1 未找到
	eng.quit()
	print ('end function error_computation')


def main():
	Modelpath = 'ModelTrace'
	Codefile  = 'CodeFiles'

	# # ###--- 生成模板的 C代码 ---###
	# # model_gen()

	## 读取模板的MICA，保存数据mat ###
	fastmodel_workload('model', Modelpath)

	# # functions to implement ###
	file_list = ['crc']
	# file_list = ['cal', 'note', 'dou']
	# file_list = ['bitcnts', 'qsort', 'susan']
	for filename in file_list:
		filepath = os.path.join(os.path.dirname(__file__), os.path.join("workload_files", filename))

		# fastmodel_workload('workload', filepath)
		# clustering(filepath)
		model_selection(filepath)
		benchmark_sythesizer.benchmark_sythesizer(filepath, Codefile)

	### functions to implement ###
	# error_computation()

if __name__ == '__main__':
	main()