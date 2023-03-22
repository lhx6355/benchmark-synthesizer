% model selection with genetic algorithm, error comuptation: euclidean in kmeans

function [workloadMatrixSelected, indexSelected, classSelectedWeight] = cluster(filepath)
     pwd_list = strsplit(pwd, '\');
     if pwd_list(size(pwd_list, 2)) == "clustering"
          addpath([pwd, '\..\error_computation']);          % 只调试当前文件，应该取消注释
     else    
          cd([pwd, '\clustering']);                         % 只调试当前文件，应该注释
     end
     % --**** loading necessary data ****--%
     load([filepath '\MICA\workloadMatrix.mat'], 		'workloadMatrix');
     load([filepath '\MICA\workloadName.mat'],          'workloadName');
     rawData = workloadMatrix;
     work_load_name = strsplit(workloadName{1}, '.');
     
     new_rawData = rawData(:, 1:255);                            % 实际的rawData也是255列的
     % new_rawData = rawData(:, 1:size(rawData, 2) - 4);        % 舍去最后的四个数据
     % assert(size(rawData, 1) - 1 > 0);
     maxK = min(20, size(rawData, 1));                       % interval的数量应该大于1
     
     fprintf(strcat('Step 1: There are', 32, num2str(size(rawData, 1)), ' intervals in ',  [' ' work_load_name{1}], '\n'));
     
     %--*************************** Norm: save normMatrix for error computation ***************************--%
     normData = value2ratio(new_rawData);
     normMatrix(1, :) = min(normData);
     normMatrix(2, :) = max(normData);

     %--******************************************* MICA **************************************************--%
     workloadMatrixSelected = [];
     indexSelected = [];
     classSelectedWeight = [];
     
     %--******************************************* 不聚类了，直接返回 **************************************************--%
     if maxK == 1
          workloadMatrixSelected = new_rawData;
          indexSelected = [1];
          classSelectedWeight = [1];
          intervalsIndex = [1];
          % ***********************************  返回的三个参数  *********************************** %
          % 选取的具有代表性的点
          save([filepath '\Cluster\workloadMatrixSelected.mat'], 'workloadMatrixSelected');
          % 选取点的序号
          save([filepath '\Cluster\indexSelected.mat'], 'indexSelected');
          indexSelected = indexSelected';
          save([filepath '\Cluster\', work_load_name{1}, '_indexSelected.mat'], 'indexSelected');

          % 选取点的权重，通过interval的数量来分配，    如果interval里的inst值不一样，可能有问题。
          save([filepath '\Cluster\classSelectedWeight.mat'], 'classSelectedWeight');
          
          save([filepath '\Cluster\', work_load_name{1}, '_intervalsIndex.mat'], 'intervalsIndex');
          save([filepath '\Cluster\', work_load_name{1}, '_new_rawData.mat'], 'new_rawData');

          save([filepath '\Cluster\normMatrix.mat'], 'normMatrix');      
          return     
     end


     maxBIC = 0; bic_score = 0; best_weight = [];
     fprintf(strcat('Step 2: Clustering into maxK: ', 32, num2str(maxK), ' \n'));
     for runNumber = 1 : maxK
          dimensionX = 1; dimensionY = runNumber;
          %% ***********************************  first part: SOM  ***********************************%
          % Normalized according to the dimensions  mapminmax：归一化处理 是将矩阵的每一行处理成[-1,1]区间,这里通过转换行列式，使得每一归[-1,1]
          % 在按列进行归一化的时候，也就消除了MICA之间由于数量级差异过大的问题
          Ptrain = mapminmax(new_rawData')';
          % Ptrain1 = mapminmax(newData')';
          net = selforgmap([dimensionX, dimensionY]);
          [net, tr] = train(net, Ptrain');                   % Train the Network 当最大的值为1时，可能有问题
          som_result = net(Ptrain');                         % Test  the Network
     
          som_clusterIndex = [];                                                                        % 每一个interval所属于的cluster的index
          for i = 1 : size(som_result, 2)
               som_clusterIndex(:, i) = find(som_result(:, i) == 1);                                    % each colum of som_clusterIndex saves the index of  cluster
          end
     
          som_keyIndex = []; som_keyPoint = []; som_weight = [];
          for t = 1 : dimensionX * dimensionY
               temp = find(som_clusterIndex == t);                                                      % temp是归类为1的interval在原始数组中的index
               if(isempty(temp))                                                                        % 某一个cluster可能为空
                    continue;
               end
               [IDX_sokm, C_sokm, Sumd_sokm, D_sokm] = kmeans(Ptrain(temp, :), 1);                      % [IDX_sokm, C_sokm, Sumd_sokm, D_sokm] = kmeans(ayi, 1);  D_sokm ： 从每个点到每个质心的距离，默认情况下，kmeans 使用欧几里德距离平方
               [W, DI] = sort(D_sokm);                                                                  % W : 升序排列，第一行是最小值，就是这次kmeans的cluster的中心点    DI ： 该值所在原数组的index
               som_weight = [som_weight, size(temp, 2)];
               som_keyIndex = [som_keyIndex, temp(DI(1, :))];                                           % 获得在全部interval中的index，D1中的index只是该cluster的
               som_keyPoint = [som_keyPoint; Ptrain(temp(DI(1, :)), :)]; 
          end
     
     
          %% ***********************************  second part: kmeans  ***********************************%
          na = find(isnan(som_keyPoint(:, 2)));
          som_keyPoint(na, :) = [];
          kmeanscentre = som_keyPoint;
          k = size(kmeanscentre, 1);
          % Start : 一种选择初始簇质心位置（即种子）的方法 | D - 从每个点到每个质心的距离
          [IDX, C, SUMD, D] = kmeans(Ptrain, k, 'Start', kmeanscentre);  
          % sort(X)对X的元素进行升序排序， sortIdx返回索引序列，它表示sortDist中的元素与D中元素的对应。
     
          %% ***********************************  third part: BIC  ***********************************%
          [R, dim] = size(new_rawData);   dist = 0;
          for i = 1 : R
               dist = dist + D(i, IDX(i));
          end

          sigma2 = dist / (R * dim);  PI = 3.14159265358979;  likelihood = - log(2.0 * PI) / 2.0 - dim * (log(sigma2) + 1) / 2.0 - log(R);
          weight = zeros(1, k);
          for i = 1 : size(IDX, 1)
               weight(IDX(i)) = weight(IDX(i)) + 1;
          end

          likelihood = likelihood * R;
          for i = 1 : k
               wt = weight(i);
               likelihood = likelihood + log(wt) * wt;
          end
     
          numParameters = (k - 1) + k * dim + 1;   penalty = numParameters / 2.0 * log(R);
          bic_score = likelihood - penalty;
          fprintf(strcat('        runNumber : ', 32, num2str(runNumber), ' bic_score : ', 32, num2str(bic_score), ' \n'));

          %% ***********************************  forth part: Update  ***********************************%
          if(maxBIC == 0 || bic_score > maxBIC)
               maxBIC = bic_score;
               best_runNumber = runNumber;
               [sortDist, sortIdx] = sort(D);
               ctrIdx = sortIdx(1, :);     
               intervalsIndex = IDX;                                                       % ctrIdx 中心在原数据中的 index
               indexSelected = ctrIdx;                                               % ctrIdx 中心在原数据中的 index
               workloadMatrixSelected = new_rawData(ctrIdx, :);
               classSelectedWeight = zeros(1, max(IDX));
               for i = 1 : max(IDX)
                    classSelectedWeight(i) = length(find(IDX == i));
               end
          end
     end
     fprintf(strcat('        The Best runNumber is : ', 32, num2str(best_runNumber), ' bic_score : ', 32, num2str(maxBIC), ' \n'));
     
     % ***********************************  返回的三个参数  *********************************** %
     % 选取的具有代表性的点
     save([filepath '\Cluster\workloadMatrixSelected.mat'], 'workloadMatrixSelected');
     % 选取点的序号
     save([filepath '\Cluster\indexSelected.mat'], 'indexSelected');
     indexSelected = indexSelected';
     save([filepath '\Cluster\', work_load_name{1}, '_indexSelected.mat'], 'indexSelected');

     % 选取点的权重，通过interval的数量来分配，    如果interval里的inst值不一样，可能有问题。
     save([filepath '\Cluster\classSelectedWeight.mat'], 'classSelectedWeight');
     
     save([filepath '\Cluster\', work_load_name{1}, '_intervalsIndex.mat'], 'intervalsIndex');
     save([filepath '\Cluster\', work_load_name{1}, '_new_rawData.mat'], 'new_rawData');

     save([filepath '\Cluster\normMatrix.mat'], 'normMatrix');
     