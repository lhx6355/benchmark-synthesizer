% 用于对两个mica进行对比，生成柱状图
function [err] = mica_diff()
dirname = pwd;
filepath = [dirname, 		'\mica_profiler'];
fileArray1 = dir([dirname, 	'\mica_profiler\crc.txt']);
fileArray2 = dir([dirname, 	'\mica_profiler\bench-crc.txt']);	
fileArray3 = dir([dirname, 	'\mica_profiler\bench-NewTemplate-crc.txt']);	

modelMatrix = [];
for n = 1: length(fileArray1)
    modelMatrix = [modelMatrix; dlmread([filepath, '\', fileArray1(n).name])];			% 多个文件中的数据读入到一个数组里
end
modelMatrix1 = sum(modelMatrix, 1);
size(modelMatrix1)
instNum1 = modelMatrix1(size(modelMatrix1, 2));

modelMatrix = [];
for n = 1: length(fileArray2)
    modelMatrix = [modelMatrix; dlmread([filepath, '\', fileArray2(n).name])];			% 多个文件中的数据读入到一个数组里
end
modelMatrix2 = sum(modelMatrix, 1);
instNum2 = modelMatrix2(size(modelMatrix2, 2));

modelMatrix = [];
for n = 1: length(fileArray3)
    modelMatrix = [modelMatrix; dlmread([filepath, '\', fileArray3(n).name])];			% 多个文件中的数据读入到一个数组里
end
modelMatrix3 = sum(modelMatrix, 1);
instNum2 = modelMatrix3(size(modelMatrix3, 2));

ldGlobalAddrDist1 = modelMatrix1(:,159:170);
stGlobalAddrDist1 = modelMatrix1(:,183:194);
GlobalAddrDist1 = ldGlobalAddrDist1 + stGlobalAddrDist1;
GlobalAddrDist1 = GlobalAddrDist1 ./ sum(GlobalAddrDist1);
cPathLength1       = modelMatrix1(:,15:55);
depGraphDist1      = modelMatrix1(:,56:85);



ldGlobalAddrDist2 = modelMatrix2(:,159:170);
stGlobalAddrDist2 = modelMatrix2(:,183:194);
GlobalAddrDist2 = ldGlobalAddrDist2 + stGlobalAddrDist2;
GlobalAddrDist2 = GlobalAddrDist2 ./ sum(GlobalAddrDist2);

cPathLength2       = modelMatrix2(:,15:55);
depGraphDist2      = modelMatrix2(:,56:85);


ldGlobalAddrDist3 = modelMatrix3(:,159:170);
stGlobalAddrDist3 = modelMatrix3(:,183:194);
GlobalAddrDist3 = ldGlobalAddrDist3 + stGlobalAddrDist3;
GlobalAddrDist3 = GlobalAddrDist3 ./ sum(GlobalAddrDist3);

cPathLength3       = modelMatrix3(:,15:55);
depGraphDist3      = modelMatrix3(:,56:85);

figure(1);
ytickformat('percentage');

bar([GlobalAddrDist1 .* 100; GlobalAddrDist2.* 100; GlobalAddrDist3.* 100]');
% set(gca, 'yscale', 'log');
legend('原程序', '旧Template', '新Template')

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
figure(2);
% bar([GlobalAddrDist1; GlobalAddrDist2]');
bar(GlobalAddrDist1);
figure(3);
bar(GlobalAddrDist2);

%     ldGlobalReuseDistAll=sum(valueVector(:,111:122),2);
%     ldLocalReuseDistAll=sum(valueVector(:,123:134),2);
%     stGlobalReuseDistAll=sum(valueVector(:,135:146),2);
%     stLocalReuseDistAll=sum(valueVector(:,147:158),2);
%     ldGlobalAddrDistAll=sum(valueVector(:,159:170),2);
%     ldLocalAddrDistAll=sum(valueVector(:,171:182),2);
%     stGlobalAddrDistAll=sum(valueVector(:,183:194),2);
%     stLocalAddrDistAll=sum(valueVector(:,195:206),2);

err = 0;
return