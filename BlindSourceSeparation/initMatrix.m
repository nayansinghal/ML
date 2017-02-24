function [ W ] = initMatrix( mixedSignals, NumOfSamples )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
NumOfSignals = size(mixedSignals,1);

% generate random matrix with values in range [0-0.1].
W = 0.1 * rand(NumOfSamples,NumOfSignals);

end

