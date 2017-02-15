function [ V ] = RescaleRow( V , a, b)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
    V = (V-min(V))*(b-a)/(max(V)-min(V)) + a;
end

