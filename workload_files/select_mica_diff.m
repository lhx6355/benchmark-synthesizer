% 对聚类算法选出的interval的MICA与所在cluster的均值进行对比，观察interval的代表性

function [] = select_mica_diff()
    path_name = 'dou'
    workload_name = 'dou';
    
    
    load([path_name, '\Cluster\', workload_name, '_indexSelected.mat'], 		'indexSelected');
    load([path_name, '\Cluster\', workload_name, '_intervalsIndex.mat'], 		'intervalsIndex');
    load([path_name, '\Cluster\', workload_name, '_new_rawData.mat'],           'new_rawData');
    
    num = size(indexSelected, 1);
    intervals_num = zeros(num, 1);
    intervals_sum = zeros(num, size(new_rawData, 2));                       % 对相同的cluster中的interval求和
    intervals_select = new_rawData(indexSelected, :);
    for i = 1 : size(new_rawData, 1)
        intervals_sum(intervalsIndex(i), :) = intervals_sum(intervalsIndex(i), :) + new_rawData(i, :);
        intervals_num(intervalsIndex(i)) = intervals_num(intervalsIndex(i)) + 1;
    end
    intervals_avg  = intervals_sum ./ intervals_num;
    
    for i = 1 : num
        figure(i); bar([intervals_avg(i, :); intervals_select(i, :)]');
        set(gca, 'yscale', 'log');
        legend('聚类中平均MICA', '代表性的Interval的MICA');
    end 
end


