% 收集生成的Template中所有的MICA的统计信息
function [err] = instnum()
dirname = pwd;
filepath = [dirname, 		'\model_profiler2'];	
fileArray = dir([dirname, 	'\model_profiler2\*txt']);	

modelName = {};
modelMatrix = [];
for n = 1: length(fileArray)
    modelMatrix = [modelMatrix; dlmread([filepath, '\', fileArray(n).name])];			% 多个文件中的数据读入到一个数组里
    modelName{n, 1} = fileArray(n).name;
end

instnum = modelMatrix(:, size(modelMatrix, 2));
cPathLength = modelMatrix(:, 15:55);
depGraphDist = modelMatrix(:,56:85);
loadspac = modelMatrix(:, 159:170);
storespac = modelMatrix(:, 183:194);

cPath_arr = var(cPathLength);
depGraph_arr = sum(depGraphDist);
load_arr = var(loadspac, 1);
store_arr = sum(storespac);

bar(cPath_arr);

arr = zeros(1, 7);
for i = 1 : length(instnum)
    if instnum(i) < 50000
        arr(1) = arr(1) + 1;
    elseif  (50000 <= instnum(i)) && (instnum(i) < 60000)
        arr(2) = arr(2) + 1;
    elseif  (60000 <= instnum(i)) && (instnum(i) < 70000)
        arr(3) = arr(3) + 1;       
    elseif  (70000 <= instnum(i)) && (instnum(i) < 80000)
        arr(4) = arr(4) + 1;        
    elseif  (80000 <= instnum(i)) && (instnum(i) < 90000)
        arr(5) = arr(5) + 1;   
    elseif  (90000 <= instnum(i)) && (instnum(i) < 100000)
        arr(6) = arr(6) + 1; 
    else
        arr(7) = arr(7) + 1; 
    end
end
bar(arr);
ax = gca;
ax.XTickLabel = {'50K<','50-60K','60-70K','70-80K','80-90K','90-100K','>100K'}

err = 0;
return