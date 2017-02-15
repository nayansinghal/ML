function [ X ] = mixSignals( sounds, numOfSignals, NumOfSamples, index)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
% TODO: randomly select the samples
W = rand(numOfSignals, NumOfSamples);
normr(W);
X = W * sounds(index, :);
end

