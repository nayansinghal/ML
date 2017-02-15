function [  ] = plotResults( U, X, Y )
%UNTITLED8 Summary of this function goes here
%   Detailed explanation goes here
plotWaves(U, 'original signals');
plotWaves(X, 'Mixed signals');
plotWaves(Y, 'Extracted signals');

end

