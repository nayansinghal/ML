function [ A ] = RescaleMatrix( A, a, b )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
for i = 1:1:size(A,1)
    A(i,:) = rescaleRow(A(i,:), a,b);
end;
end

