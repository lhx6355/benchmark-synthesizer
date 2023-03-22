%	Included angle of two arrays
%	angle = included_angle(vectorA, vectorB), for 1-by-N array vectorA and 1-by-N array vectorB,
%	returns the included angle of two arrays.

%	Angle is in the form of 360, not 2 * pi. The value range is (0, 90], and is float number.
%	If vectorA or vectorB is zero arrays, then the angle is set to 90.

%	Copyright bruceleo92
%	$Revision 1.0 $  $Date: 2017/03/01 $
%	Third-party function.


function [ angle ] = included_angle( vectorA, vectorB )

if (sum(vectorA) == 0) || (sum(vectorB) == 0)
    angle = 90;
else
    angle = acos(dot(vectorA, vectorB) / norm(vectorA) / norm(vectorB)) / pi * 180;
end

