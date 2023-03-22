%  function txt2mat converts the fastmodel profiler of worloads/models/benchmarks into MICA(micro-independent characteristics of architecture) matrix
%  and save the mapping relationships of file to the matrix in xxName.mat
%  Copyright bruceleo92
%  $Revision 2.0 $  $Date: 2023/03/03 $
%  Third-party function.

function [matrix, name] = txt2mat(profilerType, filepath)
	cd([pwd, '\fastmodel_workload']);					% 路径由 run.py -> fastmodel_workload
	switch profilerType
		case 'model'
			fileArray = dir(['..\template_files\ModelTrace', '\*txt']);	
		case 'workload'
			fileArray = dir([filepath '\MICA\Trace_Summarymica', '\*txt']);	
	end
	modelName = {};
	modelMatrix = [];
	for n = 1: length(fileArray)
		fprintf(strcat('accessing file  ', num2str(n), '\n'))
		modelMatrix = [modelMatrix; dlmread([fileArray(n).folder, '\', fileArray(n).name])];			% 多个文件中的数据读入到一个数组里
		modelName{n, 1} = fileArray(n).name;
	end

	% select 255 effective dimensions from 261 dimensions
	modelMatrix = [modelMatrix(:, 1: 255)];
	name = modelName;
	matrix = modelMatrix;

	switch profilerType
		case 'model'
			save('..\template_files\ModelMat\modelMatrix.mat', 'modelMatrix');
			save('..\template_files\ModelMat\modelName.mat', 'modelName');
		case 'workload'
			workloadMatrix = modelMatrix;
			workloadName = modelName;
			save([filepath '\MICA\workloadMatrix.mat'], 'workloadMatrix');
			save([filepath '\MICA\workloadName.mat'], 'workloadName');
	end
return