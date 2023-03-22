% convert a 1-by-255 vector of values to 1-by-255 vector of ratios of several classes
% 在各个MICA在其自身的向量维度上归一化
function [ ratioVector ] = value2ratio(valueVector)
    % Convert rawData's values of each dimension to weights according to seven
    % microarchitecture-independent characteristics(MICA).
    % 获取各个维度的数据
    if size(valueVector, 2) < 255
        printf("erroe!!\n");
    end
    InstAll             = sum(valueVector(:,1:14),2);
    cPathLength         = sum(valueVector(:,15:55),2);
    depGraphDistAll     = sum(valueVector(:,56:85),2);
    RegReadAll          = sum(valueVector(:,[86,88]),2);
    RegWriteAll         = sum(valueVector(:,[87,89,90]),2);
    fetchReuseDistAll   = sum(valueVector(:,91:100),2);
    fetchAddrDistAll    = sum(valueVector(:,101:110),2);
    ldGlobalReuseDistAll= sum(valueVector(:,111:122),2);
    ldLocalReuseDistAll = sum(valueVector(:,123:134),2);
    stGlobalReuseDistAll= sum(valueVector(:,135:146),2);
    stLocalReuseDistAll = sum(valueVector(:,147:158),2);
    ldGlobalAddrDistAll = sum(valueVector(:,159:170),2);
    ldLocalAddrDistAll  = sum(valueVector(:,171:182),2);
    stGlobalAddrDistAll = sum(valueVector(:,183:194),2);
    stLocalAddrDistAll  = sum(valueVector(:,195:206),2);
    BasicBlockAll       = sum(valueVector(:,207:221),2);
    branchesAll         = sum(valueVector(:,222:224),2);
    addrBranchesAll     = sum(valueVector(:,226:240),2);
    serialBlockSizeAll  = sum(valueVector(:,241:255),2);
    repmat(InstAll,1,14);
    ratioVector(:,1:14)     = valueVector(:,1:14)./repmat(InstAll,1,14);
    ratioVector(:,15:55)    = valueVector(:,15:55)./repmat(cPathLength,1,41);
    ratioVector(:,56:85)    = valueVector(:,56:85)./repmat(depGraphDistAll,1,30);
    ratioVector(:,86)       = RegReadAll./(RegReadAll+RegWriteAll);
    ratioVector(:,87)       = RegWriteAll./(RegReadAll+RegWriteAll);
    ratioVector(:,88:97)    = valueVector(:,91:100)./repmat(fetchReuseDistAll,1,10);
    ratioVector(:,98:107)   = valueVector(:,101:110)./repmat(fetchAddrDistAll,1,10);
    ratioVector(:,108:119)  = valueVector(:,111:122)./repmat(ldGlobalReuseDistAll,1,12);
    ratioVector(:,120:131)  = valueVector(:,123:134)./repmat(ldLocalReuseDistAll,1,12);
    ratioVector(:,132:143)  = valueVector(:,135:146)./repmat(stGlobalReuseDistAll,1,12);
    ratioVector(:,144:155)  = valueVector(:,147:158)./repmat(stLocalReuseDistAll,1,12);
    ratioVector(:,156:167)  = valueVector(:,159:170)./repmat(ldGlobalAddrDistAll,1,12);
    ratioVector(:,168:179)  = valueVector(:,171:182)./repmat(ldLocalAddrDistAll,1,12);
    ratioVector(:,180:191)  = valueVector(:,183:194)./repmat(stGlobalAddrDistAll,1,12);
    ratioVector(:,192:203)  = valueVector(:,195:206)./repmat(stLocalAddrDistAll,1,12);
    ratioVector(:,204:218)  = valueVector(:,207:221)./repmat(BasicBlockAll,1,15);
    ratioVector(:,219)      = valueVector(:,222)./branchesAll;
    ratioVector(:,220)      = valueVector(:,223)./branchesAll;
    ratioVector(:,221)      = valueVector(:,224)./branchesAll;
    ratioVector(:,222)      = valueVector(:,225)./branchesAll;
    ratioVector(:,223:237)  = valueVector(:,226:240)./repmat(addrBranchesAll,1,15);
    ratioVector(:,238:252)  = valueVector(:,241:255)./repmat(serialBlockSizeAll,1,15);

    index = find(isnan(ratioVector));
    ratioVector(index) = 0;
    return
end