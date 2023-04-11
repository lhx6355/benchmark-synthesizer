% 最大的分布占比

function [] = template_check()
    load(['ModelMat\modelMatrix.mat'], 		'modelMatrix');
    load(['ModelMat\modelName.mat'], 		'modelName');
    
    addpath([pwd, '\..\error_computation']);
    modelMatrix = [modelMatrix(:, 1: 255)];
%     modelMatrix = value2ratio(modelMatrix, {'ALL'});
    
    Inst  = modelMatrix(:,  1:14);
    cPath = modelMatrix(:, 15:55);
    reg   = modelMatrix(:, 56:85);
    
    [Inst_max, Inst_index] = max(Inst');
    [cPath_max, cPath_index] = max(cPath');
    [reg_max, reg_index] = max(reg');
    Inst_index = Inst_index';
    cPath_index = cPath_index';
    reg_index = reg_index';
    temp = [modelName, num2cell(Inst_index), num2cell(cPath_index),  num2cell(reg_index)];

%% 去掉过于突出的值，
%     ans = [];
%     count_15 = 0; count_13 = 0; count_14 = 0; count_1 = 0; count_6 = 0; count_7 = 0;
%     for i = 1 : size(temp)
%        cPath = cell2mat(temp(i, 3)); 
%        if (cPath == 15 && count_15 > 50) || (cPath == 13 && count_13 > 50) || (cPath == 14 && count_14 > 50) || (cPath == 1 && count_1 > 50) || (cPath == 6 && count_6 > 50) || (cPath == 7 && count_7 > 50)
%            continue
%        else
%            if cPath == 15
%                count_15 = count_15 + 1;
%            elseif cPath == 13
%                count_13 = count_13 + 1;
%            elseif cPath == 14
%                count_14 = count_14 + 1;
%            elseif cPath == 1
%                count_1 = count_1 + 1;
%            elseif cPath == 6
%                count_6 = count_6 + 1;
%            elseif cPath == 7
%                count_7 = count_7 + 1;
%            end
%            ans = [ans; temp(i, :)];
%        end
%     end
% % 复制到新的文件夹
%     CodeFiles_name  = 'CodeFiles';
%     ModelTrace_name = 'ModelTrace';
%     CodeFiles_new  = ['CodeFiles',  '-', num2str(size(ans, 1))];
%     ModelTrace_new = ['ModelTrace', '-', num2str(size(ans, 1))];
%     mkdir(CodeFiles_new);
%     mkdir(ModelTrace_new);
%     for i = 1 : size(ans, 1)
%         name = cell2mat(ans(i, 1));
%         path_dir = [pwd, '\', ModelTrace_name, '\', name];
%         path_aim = [pwd, '\', ModelTrace_new];
%         copyfile(path_dir, path_aim);
%         
%         name = split(name, '.');
%         name = split(name(2), '-');
%         path_dir = [pwd, '\', CodeFiles_name, '\', cell2mat(name(1)), '.c'];
%         path_aim = [pwd, '\', CodeFiles_new];
%         copyfile(path_dir, path_aim);
%     end

%%   指令混合比
%     Inst_dis  = zeros(1, 14);
%     for i = 1 : size(Inst_index, 1)
%         Inst_dis(Inst_index(i, 1)) = Inst_dis(Inst_index(i, 1)) + 1;
%     end
%     bar(Inst_dis);



%%   关键路径长度
    cPath_dis = zeros(1, 41);
    for i = 1 : size(cPath_index, 1)
        cPath_dis(cPath_index(i, 1)) = cPath_dis(cPath_index(i, 1)) + 1;
    end
    figure(1); bar(cPath_dis);

%%   访存相关

%     % 去掉过于突出的值
%     ldGlobalAddrDist  = modelMatrix(:, 159:170); [ldGlobalAddrDist_max,  ldGlobalAddrDist_index]  = max(ldGlobalAddrDist');  ldGlobalAddrDist_index  = ldGlobalAddrDist_index';
%     stGlobalAddrDist  = modelMatrix(:, 183:194); [stGlobalAddrDist_max,  stGlobalAddrDist_index]  = max(stGlobalAddrDist');  stGlobalAddrDist_index  = stGlobalAddrDist_index';   
%     AddrDist = [ldGlobalAddrDist_index stGlobalAddrDist_index];
%     mem_temp = [modelName, num2cell(ldGlobalAddrDist_index), num2cell(stGlobalAddrDist_index)];
%     ans = [];
%     count = 0;
% 	for i = 1 : size(mem_temp, 1)
%        dist = cell2mat(mem_temp(i, 3)); 
%        if dist == 1 && count > 50
%            continue
%        else
%            if dist == 1
%                count = count + 1;
%            end
%            ans = [ans; temp(i, :)];
%        end
%     end
%     % 复制到新的文件夹
%     CodeFiles_name  = 'CodeFiles-474';
%     ModelTrace_name = 'ModelTrace-474';
%     CodeFiles_new  = ['CodeFiles',  '-', num2str(size(ans, 1))];
%     ModelTrace_new = ['ModelTrace', '-', num2str(size(ans, 1))];
%     mkdir(CodeFiles_new);
%     mkdir(ModelTrace_new);
%     for i = 1 : size(ans, 1)
%         name = cell2mat(ans(i, 1));
%         path_dir = [pwd, '\', ModelTrace_name, '\', name];
%         path_aim = [pwd, '\', ModelTrace_new];
%         copyfile(path_dir, path_aim);
%         
%         name = split(name, '.');
%         name = split(name(2), '-');
%         path_dir = [pwd, '\', CodeFiles_name, '\', cell2mat(name(1)), '.c'];
%         path_aim = [pwd, '\', CodeFiles_new];
%         copyfile(path_dir, path_aim);
%     end

    ldGlobalReuseDist = modelMatrix(:, 111:122); [ldGlobalReuseDist_max, ldGlobalReuseDist_index] = max(ldGlobalReuseDist'); ldGlobalReuseDist_index = ldGlobalReuseDist_index';
    stGlobalReuseDist = modelMatrix(:, 135:146); [stGlobalReuseDist_max, stGlobalReuseDist_index] = max(stGlobalReuseDist'); stGlobalReuseDist_index = stGlobalReuseDist_index';
    ldGlobalAddrDist  = modelMatrix(:, 159:170); [ldGlobalAddrDist_max,  ldGlobalAddrDist_index]  = max(ldGlobalAddrDist');  ldGlobalAddrDist_index  = ldGlobalAddrDist_index';
    stGlobalAddrDist  = modelMatrix(:, 183:194); [stGlobalAddrDist_max,  stGlobalAddrDist_index]  = max(stGlobalAddrDist');  stGlobalAddrDist_index  = stGlobalAddrDist_index';   

    mem_temp = [modelName, num2cell(ldGlobalReuseDist_index),  num2cell(stGlobalReuseDist_index), num2cell(ldGlobalAddrDist_index), num2cell(stGlobalAddrDist_index)];
    ldGlobalReuseDist_dis = zeros(1, 12); stGlobalReuseDist_dis = zeros(1, 12); ldGlobalAddrDist_dis = zeros(1, 12); stGlobalAddrDist_dis = zeros(1, 12);
    for i = 1 : size(ldGlobalReuseDist_index, 1)
        ldGlobalReuseDist_dis(ldGlobalReuseDist_index(i, 1)) = ldGlobalReuseDist_dis(ldGlobalReuseDist_index(i, 1)) + 1;
        stGlobalReuseDist_dis(stGlobalReuseDist_index(i, 1)) = stGlobalReuseDist_dis(stGlobalReuseDist_index(i, 1)) + 1;
        ldGlobalAddrDist_dis(ldGlobalAddrDist_index(i, 1)) = ldGlobalAddrDist_dis(ldGlobalAddrDist_index(i, 1)) + 1;
        stGlobalAddrDist_dis(stGlobalAddrDist_index(i, 1)) = stGlobalAddrDist_dis(stGlobalAddrDist_index(i, 1)) + 1;
    end
    figure(2);bar(ldGlobalReuseDist_dis);
    figure(3);bar(stGlobalReuseDist_dis);
    figure(4);bar(ldGlobalAddrDist_dis);
    figure(5);bar(stGlobalAddrDist_dis);
    
end
