load('icaTest.mat');
NumOfSignals = 3;
X = A*U;

learningRate = 0.01;
numIters = 100;

Y = ICA(learningRate, numIters, X, NumOfSignals);
plotResults(X, Y, U);