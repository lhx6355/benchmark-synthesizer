% model selection with genetic algorithm, error comuptation: euclidean in kmeans
function [ modelSelected ] = model_select_genetic_eu(filepath)
	pwd_list = strsplit(pwd, '\');
	if pwd_list(size(pwd_list, 2)) == "model_selection"			
		addpath([pwd, '\..\error_computation']);            % 单独文件调试时
	else    
		cd([pwd, '\model_selection']);                  	% 由run.py调试时
	end

	% global 
	global work_load_name popSize chromoSize generationNum positiveBit eliteFactor crossFactor mutateFactor modelMatrix normMatrix;

	% --**** loading necessary data ****--%
	load(['..\template_files\ModelMat\modelMatrix.mat'], 		'modelMatrix');
	load([filepath, '\MICA\workloadName.mat'], 					'workloadName');
	load([filepath, '\Cluster\workloadMatrixSelected.mat'], 	'workloadMatrixSelected');
	load([filepath, '\Cluster\normMatrix.mat'], 				'normMatrix');


	work_load_name = strsplit(workloadName{1}, '.');
	% if ~exist(['Errer/' work_load_name{1}], 'dir')
	% 	mkdir(['Errer/' work_load_name{1}]);
	% end

	% genetic algorithm parameters
	popSize = 100;    					% population size
	chromoSize = size(modelMatrix, 1);	% size of model library
	generationNum = 500;    			% iteration times of genetic algorithm                  迭代次数
	positiveBit = 50;   				% positive gene bits(selected number of models)         初始化的时候，前100个model匹配
	eliteFactor = 0.1;    				% elite ratio to store into child generation		 	精英率
	crossFactor = 0.6;    				% cross over factor, gene bits ratio for cross over  	交叉率
	mutateFactor = 0.8;    				% mutate factor, gene bits ratio for mutate			 	变异率

	[MODEL_ROW, MODEL_COL] = size(modelMatrix);
	[WORKLOAD_ROW, WORKLOAD_COL] = size(workloadMatrixSelected);

	% 最后的输出
	modelSelected = zeros(WORKLOAD_ROW, MODEL_ROW); 	% 33 * 25933
	for slice = 1: WORKLOAD_ROW								% 每个切片都做一次对所有的程序模板的遗传算法适配
		target = workloadMatrixSelected(slice, :);
		[minErr, bestIndividual] = GA(slice, WORKLOAD_ROW, target);
		modelSelected(slice, :) = bestIndividual;
	end

	save([filepath '\Select\modelSelected.mat'], 'modelSelected');


	function [ minErr, bestIndividual ] = GA(slice, WORKLOAD_ROW, target)
		% initialize the population
		pop = initialize();
		minErr = 5000000;																						    % 如果所有的误差都大于5000，则select为空 
		bestGeneration = 0;
		bestIndividual = zeros(1, chromoSize);
		Err_iter = zeros(generationNum, 2);
		for iter = 1: generationNum
			fprintf(strcat('working on workload',  [' ', work_load_name{1}, ' '], ' slice: ', num2str(slice), '/ ',  num2str(WORKLOAD_ROW), '   '));	
			fprintf(strcat('  iteration time: ', num2str(iter), '    '));
			fprintf(strcat('  bestGeneration: ', num2str(bestGeneration), '    '));
			fprintf(strcat('  minErr is:', num2str(minErr), '   '));
			[pop, bestFatherPop, fitnessValue, bestFatherFitness] = fitness_and_sorting(target, pop);% 所有染色体对某一个workload slice的误差，返回误差的倒数：适应度, % 选择 对pop以及fitnessValue重排序，根据精英比例，选出最适应的几个染色体bestFatherPop   bestFitness ： 只有一个值
					posIndex = find(pop(1, :) == 1);                                                				% 随着迭代的进行，感兴趣的基因片段会越来越少??
			[pop] = crossover(pop, fitnessValue);									% 交叉
					posIndex = find(pop(1, :) == 1);
			[pop] = mutation(pop);                                              % 变异
					posIndex = find(pop(1, :) == 1);
			[pop, ~, fitnessValue, bestFitness] = fitness_and_sorting(target, pop);		% 重新计算适应度
			currentErr = 1 / bestFitness;																			% 本次的最优值，在FatherPop替换回之前的

			[pop] = selection(bestFatherPop, pop);											% 为选出的bestFatherPop替换回pop，替换掉pop中最差的

			fprintf(strcat('  current error is:', num2str(currentErr), '\n'));
			if currentErr < minErr || currentErr <= 0.1
				minErr = currentErr;                                                                                % minErr = bestFitness; ??
				bestGeneration = iter;
				bestIndividual = pop(1, :);
				micaMatch = [sum(modelMatrix(find(bestIndividual == 1), :)); target];								% 当前遗传算法得到的最优模板 MICA 和
			end
			Err_iter(iter, :) = [minErr, currentErr];
		end
		Err_iter_name = [filepath '\Select\', work_load_name{1}, '_Erriter_', num2str(slice), '.mat'];
        MICA_match_name = [filepath '\Select\', work_load_name{1}, '_Match_', num2str(slice), '.mat'];
		save(Err_iter_name, 'Err_iter');																	% 记录迭代err的变化
        save(MICA_match_name, 'micaMatch');																	% 记录迭代err的变化
		return
	end


	% initialize the population, returned with original population with popSize individuals
	% 随机初始化originalPop：有positiveBit个model匹配
	function [ originalPop ] = initialize()
		individual = [ones(1, positiveBit), zeros(1, chromoSize - positiveBit)];
		for i = 1 : popSize
			index = randperm(chromoSize);
			originalPop(i, :) = individual(index);
		end
		return
	end

	function [ pop ] = crossover(pop, fitnessValue)
		roulette = cumsum(fitnessValue) / sum(fitnessValue);						% cumsum 累加和 / sum 总和    最后一个元素是1   roulette ： 轮盘赌
		selectedIndex(popSize) = 0;
		% select individual of pop size in roulette way
		for i = 1: popSize
		% parfor i = 1: popSize
			randNum = rand();														% 返回一个在区间 (0,1) 内均匀分布的随机数
			index(i) = find(roulette >= randNum, 1, 'first');						% index : 第一个大于randNum的位置
		end
		pop = pop(index, :);														% 被随机数选中的染色进行替换

		% cross over operation
		crossNum = round(chromoSize * crossFactor);
		for j = 1: 2: popSize
		% parfor j = 1: 2: popSize
			individual1 = pop(j, :);
			individual2 = pop(j + 1, :);
			% cross over operation
			crossIndex = randperm(chromoSize, crossNum);							% crossIndex ： 要交换的index
			tempBit = individual1(crossIndex);
			individual1(crossIndex) = individual2(crossIndex);
			individual2(crossIndex) = tempBit; 
			pop(j, :) = individual1;
			pop(j + 1, :) = individual2;
		end
		return
	end
	% 
	% function [ pop ] = mutation(popSize, pop, positiveBit, mutateFactor)
	% 	for t = 1: popSize
	% 		individual = pop(t, :);
	% 		
	% 		negIndex = find(individual == 0);
	% 		posIndex = find(individual == 1);
	%       negNumber = size(negIndex, 2);
	%       posNumber = size(posIndex, 2);
	% %       negCrossBit = negIndex(randperm(negNumber, round(negNumber * mutateFactor)));                         % 产生1 - n 中K个随机数，不重复
	% % 		posCrossBit = posIndex(randperm(posNumber, round(posNumber * mutateFactor)));
	%         num = min(negNumber, posNumber);
	%       negCrossBit = negIndex(randperm(negNumber, round(num * mutateFactor)));                         % 产生1 - n 中K个随机数，不重复
	% 		posCrossBit = posIndex(randperm(posNumber, round(num * mutateFactor)));        
	% 		individual(posCrossBit) = 0;
	% 		individual(negCrossBit) = 1;
	% 		pop(t, :) = individual;
	% 	end
	% 	return
	% end

	% 存在问题： posIndex的大小可能会小于mutateNum，此时会出现数组越界的问题
	function [ pop ] = mutation(pop)
		mutateNum = round(positiveBit * mutateFactor / 2) * 2;
		parfor t = 1: popSize
			individual = pop(t, :);
			negIndex = find(individual == 0);
			posIndex = find(individual == 1);
			negCrossBit = negIndex(randperm(min(mutateNum, size(negIndex, 2))));
			posCrossBit = posIndex(randperm(min(mutateNum, size(posIndex, 2))));
			individual(posCrossBit) = 0;
			individual(negCrossBit) = 1;
			pop(t, :) = individual;
		end
		return
	end

	% compute the fitness value of the population -- done
	function [ fitnessValue ] = fitness(target, pop)
		fitnessValue(popSize) = 0;
		parfor i = 1: popSize
			posIndex = find(pop(i, :) == 1);
			if size(posIndex, 2) == 1                                               % 当posIndex只有1个感兴趣的基因片段时，sum失去了本来的意义，函数出错
				individual = modelMatrix(posIndex, :);
			else
				individual = sum(modelMatrix(posIndex, :));							% 当前染色体适配的所有model的MICA对每一个维度求和，1 * 255
			end
			err = error_eu(individual, target, normMatrix);                         % 欧氏距离误差
			fitnessValue(i) = 1 / err;
		end
		return
	end

	% return pop sorted descendly by fitness value and best pop of elite factor 
	function [ pop, bestPop, fitnessValue, bestFitness ] = sorting(fitnessValue, pop)
		[fitnessValue, sortIndex] = sort(fitnessValue, 'descend');
		pop = pop(sortIndex, :);											% 根据适应情况（误差的倒数）重新排序
		eliteNum = round(popSize * eliteFactor);
		bestPop = pop(1: eliteNum, :);
		bestFitness = fitnessValue(1);
		return
	end

	% 整合两个函数
	function [ pop, bestPop, fitnessValue, bestFitness ] = fitness_and_sorting(target, pop)
		fitnessValue = fitness(target, pop);									% 所有染色体对某一个workload slice的误差，返回误差的倒数：适应度
		[pop, bestPop, fitnessValue, bestFitness] = sorting(fitnessValue, pop);				
		return
	end

	% 将排序后的pop中最后的染色体替换成最优秀的
	function [ pop ] = selection(bestPop, pop)
		eliteNum = round(eliteFactor * popSize);
		pop((popSize - eliteNum + 1): popSize, :) = bestPop;										% 淘汰最差的
		return
	end

end