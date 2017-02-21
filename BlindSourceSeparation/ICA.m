function [ Y, W ] = ICA( learningRate, numIters, X, NumOfSignals)
%generates independent components asumed that they are generated
% from linear combination of non-gaussian variables
NumOfSamples = size(X,1);

% generate random matrix with values in range [0-0.1].
W = 0.1 * rand(NumOfSignals,NumOfSamples);
Y = W * X;
I = eye(size(Y,1));
prevNormW = norm(W);
curNormW = prevNormW;
epsilon = 10^(-6);
normW = [];

for i = 1:1: numIters
    prevNormW = curNormW;
    sigmoid = 1./(1 + exp(-Y));
    dW = learningRate * ((I + (1-2*sigmoid) * Y')*W);
    W = W + dW;
    curNormW = norm(W);
    Y = W * X;
    normW = [normW; norm(dW)];
end;


end

