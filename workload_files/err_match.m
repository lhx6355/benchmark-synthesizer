function [] = err_match()
    path_name = 'dou';
    workload_name = 'dou';
    addpath([pwd, '\..\error_computation']);     
    num = 10;
    
    for i = 1: num
        load([path_name, '\Select\', workload_name, '_Match_',  num2str(i) , '.mat'], 		'micaMatch');
        intervals_select = micaMatch(2, :);
        intervals_Match = micaMatch(1, :);

%       %***** 转化为百分比  ILP Inst Global ALL
        intervals_select = value2ratio(intervals_select, {'ILP', 'Global'}) .* 100; 
        intervals_Match  = value2ratio(intervals_Match,  {'ILP', 'Global'}) .* 100;
        
        figure(i);  bar([intervals_select; intervals_Match]');
        legend('原interval的MICA', '算法匹配后MICA和');
    end
    
    min_err = [];
    for i = 1: num
        load([workload_name, '\Select\', workload_name, '_Erriter_', num2str(i), '.mat'], 		'Err_iter');
        min_err = [min_err; Err_iter(size(Err_iter, 1), 1)];
%         figure(i);
%         plot(Err_iter(:, 1)); hold on;
%         plot(Err_iter(:, 2)); legend('所有迭代中的Err最小值', '上次迭代中的Err最小值');
    end
   
end
