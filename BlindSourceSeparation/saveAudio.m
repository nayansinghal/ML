function [ output_args ] = saveAudio( A, title )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
    Fs = 8192
    for i = 1:1: size(A,1)
       audiowrite(strcat(title,sprintf('%d.wav',i)),A(i,:),Fs);     
    end;

end

