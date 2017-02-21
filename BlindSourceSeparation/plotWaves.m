function [ ] = plotWaves( A, title )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    A = rescaleMatrix(A, -1,1);
    fig = figure('name', title);
    color = ['r','m','b','g','k'];
    
    %plot all the signals
    for i = 1:1: size(A,1)
        subplot(size(A,1),1,i);
        plot(A(i,:))
        xlabel(sprintf('Signal %d',i));
        ylabel('Amplitude');
    end;
    saveas(fig, strcat(title,'.jpg'))
end

