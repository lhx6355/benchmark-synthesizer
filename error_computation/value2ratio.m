% convert a 1-by-255 vector of values to 1-by-255 vector of ratios of several classes
% mica_parameter 是一个cell
% 在各个MICA在其自身的向量维度上归一化
function [ ratioVector ] = value2ratio(valueVector, mica_parameter)
    % Convert rawData's values of each dimension to weights according to seven
    % microarchitecture-independent characteristics(MICA).
    % 获取各个维度的数据
    % if size(valueVector, 2) < 255
    %     printf("erroe!!\n");
    % end

    Inst                = valueVector(:,1:14);
    cPathLength         = valueVector(:,15:55);
    depGraphDist        = valueVector(:,56:85);
    RegRead             = valueVector(:,[86,88]);
    RegWrite            = valueVector(:,[87,89,90]);
    fetchReuseDist      = valueVector(:,91:100);
    fetchAddrDist       = valueVector(:,101:110);
    ldGlobalReuseDist   = valueVector(:,111:122);
    ldLocalReuseDist    = valueVector(:,123:134);
    stGlobalReuseDist   = valueVector(:,135:146);
    stLocalReuseDist    = valueVector(:,135:146);
    ldGlobalAddrDist    = valueVector(:,159:170);
    ldLocalAddrDist     = valueVector(:,171:182);
    stGlobalAddrDist    = valueVector(:,183:194);
    stLocalAddrDist     = valueVector(:,195:206);
    BasicBlock          = valueVector(:,207:221);
    branches            = valueVector(:,222:224);
    addrBranches        = valueVector(:,226:240);
    serialBlockSize     = valueVector(:,241:255);

    InstAll             = sum(Inst, 2);
    cPathLengthALL      = sum(cPathLength, 2);
    depGraphDistAll     = sum(depGraphDist, 2);
    RegReadAll          = sum(RegRead, 2);
    RegWriteAll         = sum(RegWrite, 2);
    fetchReuseDistAll   = sum(fetchReuseDist, 2);
    fetchAddrDistAll    = sum(fetchAddrDist, 2);
    ldGlobalReuseDistAll= sum(ldGlobalReuseDist, 2);
    ldLocalReuseDistAll = sum(ldLocalReuseDist, 2);
    stGlobalReuseDistAll= sum(stGlobalReuseDist, 2);
    stLocalReuseDistAll = sum(stLocalReuseDist, 2);
    ldGlobalAddrDistAll = sum(ldGlobalAddrDist, 2);
    ldLocalAddrDistAll  = sum(ldLocalAddrDist, 2);
    stGlobalAddrDistAll = sum(stGlobalAddrDist, 2);
    stLocalAddrDistAll  = sum(stLocalAddrDist, 2);
    BasicBlockAll       = sum(BasicBlock, 2);
    branchesAll         = sum(branches, 2);
    addrBranchesAll     = sum(addrBranches, 2);
    serialBlockSizeAll  = sum(serialBlockSize, 2);

    ratioVector = [];
    if ismember(mica_parameter, 'ALL')
        ratioVector(:, 1:14)     = Inst./repmat(InstAll, 1, 14);
        ratioVector(:, 15:55)    = cPathLength./repmat(cPathLengthALL, 1, 41);
        ratioVector(:, 56:85)    = depGraphDist./repmat(depGraphDistAll, 1, 30);
        ratioVector(:, 86)       = RegReadAll./(RegReadAll + RegWriteAll);
        ratioVector(:, 87)       = RegWriteAll./(RegReadAll + RegWriteAll);
        ratioVector(:, 88:97)    = fetchReuseDist./repmat(fetchReuseDistAll, 1, 10);
        ratioVector(:, 98:107)   = fetchAddrDist./repmat(fetchAddrDistAll, 1, 10);
        ratioVector(:, 108:119)  = ldGlobalReuseDist./repmat(ldGlobalReuseDistAll, 1, 12);
        ratioVector(:, 120:131)  = ldLocalReuseDist./repmat(ldLocalReuseDistAll, 1, 12);
        ratioVector(:, 132:143)  = stGlobalReuseDist./repmat(stGlobalReuseDistAll, 1, 12);
        ratioVector(:, 144:155)  = stLocalReuseDist./repmat(stLocalReuseDistAll, 1, 12);
        ratioVector(:, 156:167)  = ldGlobalAddrDist./repmat(ldGlobalAddrDistAll, 1, 12);
        ratioVector(:, 168:179)  = ldLocalAddrDist./repmat(ldLocalAddrDistAll, 1, 12);
        ratioVector(:, 180:191)  = stGlobalAddrDist./repmat(stGlobalAddrDistAll, 1, 12);
        ratioVector(:, 192:203)  = stLocalAddrDist./repmat(stLocalAddrDistAll, 1, 12);
        ratioVector(:, 204:218)  = BasicBlock./repmat(BasicBlockAll, 1, 15);
        ratioVector(:, 219)      = valueVector(:, 222)./branchesAll;
        ratioVector(:, 220)      = valueVector(:, 223)./branchesAll;
        ratioVector(:, 221)      = valueVector(:, 224)./branchesAll;
        ratioVector(:, 222)      = valueVector(:, 225)./branchesAll;
        ratioVector(:, 223:237)  = addrBranches./repmat(addrBranchesAll, 1, 15);
        ratioVector(:, 238:252)  = serialBlockSize./repmat(serialBlockSizeAll, 1, 15);
    else
        if ismember(mica_parameter, 'Inst')
            ratioVector = [ratioVector, Inst./repmat(InstAll,1,14)];
        end
        if ismember(mica_parameter, 'cPathLength')
            ratioVector = [ratioVector, cPathLength./repmat(cPathLengthALL, 1, 41)];
        end
        if ismember(mica_parameter, 'depGraphDist')
            ratioVector = [ratioVector, depGraphDist./repmat(depGraphDistAll, 1, 30)];
        end
        if ismember(mica_parameter, 'RegRead&Write')
            ratioVector = [ratioVector, RegReadAll./(RegReadAll + RegWriteAll)];
            ratioVector = [ratioVector, RegWriteAll./(RegReadAll + RegWriteAll)];
        end
        if ismember(mica_parameter, 'fetch')
            ratioVector = [ratioVector, fetchReuseDist./repmat(fetchReuseDistAll, 1, 10)];
            ratioVector = [ratioVector, fetchAddrDist./repmat(fetchAddrDistAll, 1, 10)];
        end
        if ismember(mica_parameter, 'Global')
            ratioVector = [ratioVector, ldGlobalReuseDist./repmat(ldGlobalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, stGlobalReuseDist./repmat(stGlobalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, ldGlobalAddrDist./repmat(ldGlobalAddrDistAll, 1, 12)];
            ratioVector = [ratioVector, stGlobalAddrDist./repmat(stGlobalAddrDistAll, 1, 12)];
        end
        if ismember(mica_parameter, 'Global&Local')
            ratioVector = [ratioVector, ldGlobalReuseDist./repmat(ldGlobalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, ldLocalReuseDist./repmat(ldLocalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, stGlobalReuseDist./repmat(stGlobalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, stLocalReuseDist./repmat(stLocalReuseDistAll, 1, 12)];
            ratioVector = [ratioVector, ldGlobalAddrDist./repmat(ldGlobalAddrDistAll, 1, 12)];
            ratioVector = [ratioVector, ldLocalAddrDist./repmat(ldLocalAddrDistAll, 1, 12)];
            ratioVector = [ratioVector, stGlobalAddrDist./repmat(stGlobalAddrDistAll, 1, 12)];
            ratioVector = [ratioVector, stLocalAddrDist./repmat(stLocalAddrDistAll, 1, 12)];
        end
        if ismember(mica_parameter, 'BasicBlock')
            ratioVector = [ratioVector, BasicBlock./repmat(BasicBlockAll, 1, 15)];
        end
        if ismember(mica_parameter, 'branches')
            ratioVector = [ratioVector, branches(:, 1)./branchesAll];
            ratioVector = [ratioVector, branches(:, 2)./branchesAll];
            ratioVector = [ratioVector, branches(:, 3)./branchesAll];
            ratioVector = [ratioVector, branches(:, 4)./branchesAll];
            ratioVector = [ratioVector, addrBranches./repmat(addrBranchesAll, 1, 15)];
        end
        if ismember(mica_parameter, 'serialBlockSize')
            ratioVector = [ratioVector, serialBlockSize./repmat(serialBlockSizeAll, 1, 15)];
        end
    end

    index = find(isnan(ratioVector));
    ratioVector(index) = 0;
    return
end