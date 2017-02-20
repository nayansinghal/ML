function [ data ] = Reshape( data )
%Reshape 4D image data into 2D
    [s1, s2, s3, s4] = size(data);
    data = reshape(data, s1*s2*s3, s4);
end

