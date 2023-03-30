%
function [err] = error_eu(vectorA, vectorB, normMatrix)
	ratioVectorA = value2ratio(vectorA, {'cPathLength'});					% 归一化
	ratioVectorB = value2ratio(vectorB, {'cPathLength'});
	% normedA = -1 + (ratioVectorA - normMatrix(1, :)) ./ (normMatrix(2, :) - normMatrix(1, :));
	% normedB = -1 + (ratioVectorB - normMatrix(1, :)) ./ (normMatrix(2, :) - normMatrix(1, :));
	normedA = ratioVectorA;
	normedB = ratioVectorB;

	indexA = find(isnan(normedA));
	normedA(indexA) = 0;
	indexA = find(isinf(normedA));
	normedA(indexA) = 0;
	indexB = find(isnan(normedB));
	normedB(indexB) = 0;
	indexB = find(isinf(normedB));
	normedB(indexB) = 0;

	err = norm(abs(normedA - normedB));						% 向量的欧式距离  % norm 计算范数 norm(A) 与 norm(A, 2)相同，都表示2范数。即sqrt(sum(abs(A.^2)))
	
	if sum(vectorA, 2) == 0 || sum(vectorB, 2) == 0
		err = 1;
	end
	return
end