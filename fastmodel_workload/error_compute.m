%
%  function txt2mat converts the fastmodel profiler of worloads/models/benchmarks into MICA(micro-independent characteristics of architecture) matrix
%  and save the mapping relationships of file to the matrix in xxName.mat

%  Copyright bruceleo92
%  $Revision 1.0 $  $Date: 2017/03/01 $
%  Third-party function.

function [matrix, name] = error_compute(profilerType, filename)
    filename = ['\', filename];
    cd([pwd, '\fastmodel_workload']);					% run.py -> fastmodel
    dirname = pwd;