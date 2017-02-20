function [ Accuracy ] = Test( Images, Labels, model, Mean, EVector )
%Test the image data and return accuracy

    %Transform data in EigenVector Coordinate frames
    ImagesNorm = bsxfun(@minus, double(Images), Mean);
    Images = ImagesNorm' * EVector;
    
    %Predict label for the test images
    Accuracy = sum(predict(model, Images) == Labels');
    
    %Calculate accuracy for the test images
    Accuracy = double(Accuracy *  100)/double(size(Images,1));
end

