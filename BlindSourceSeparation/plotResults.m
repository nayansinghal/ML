function [  ] = plotResults( U, X, Y , i)
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here
plotWaves(U, strcat('output/combination/original signals', num2str(i)));
plotWaves(X, strcat('output/combination/Mixed signals', num2str(i)));
plotWaves(Y, strcat('output/combination/Reconstructed signals', num2str(i)));
close all;

saveAudio(U, 'output/original signals');
saveAudio(X, 'output/Mixed signals');
saveAudio(Y, 'output/Reconstructed signals');

end

