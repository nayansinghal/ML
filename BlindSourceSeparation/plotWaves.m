function [ ] = plotWaves( A, title )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    fig = figure('name', title);
    color = ['r','m','b','g','k'];
    for i = 1:1: size(A,1)
        subplot(size(A,1),1,i);
        plot(A(i,:),color(i))
        xlabel(sprintf('Signal %d',i));
        ylabel('Amplitude');
    end;
    saveas(fig, strcat(title,'.jpg'))
end

