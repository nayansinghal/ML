clear all;
clc;
close all;

load('sounds.mat');
NumOfSignals =3;
NumOfSamples = 3;
index = [1,3,4];
U = sounds(index,:);
%X = A*U;
[mixedSignals, A] = mixSignals(sounds, NumOfSignals, NumOfSamples, index);
matrixError = [];

% Varying learning rate
for learningRate = 0.01: 0.01:0.01
    % Varying number of iterations
    for numIters = 1000:1000:100000
        
        error = 0;
        % Varying count number
        for count = 1:1:10

            [Y,W] = ICA(learningRate, numIters, mixedSignals, NumOfSamples);
            error = error + (norm(pinv(A)) - norm(W));
        end;
        matrixError = [matrixError; error/10];
    end;
end;
plot([1000:1000:100000], matrixError)
%plotResults(U, mixedSignals, Y);