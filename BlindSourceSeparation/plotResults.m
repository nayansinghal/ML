function [  ] = plotResults( U, X, Y )
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here
plotWaves(U, 'output/original signals');
plotWaves(X, 'output/Mixed signals');
plotWaves(Y, 'output/Reconstructed signals');

saveAudio(U, 'output/original signals');
saveAudio(X, 'output/Mixed signals');
saveAudio(Y, 'output/Reconstructed signals');
end

