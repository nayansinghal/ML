function [ mixedSignals, A ] = mixSignals( sounds, numOfSignals, NumOfSamples, index)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
% TODO: randomly select the samples
A = rand(numOfSignals, NumOfSamples);
normr(A);
mixedSignals = A * sounds(index, :);
end

