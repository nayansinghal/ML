clear all;
clc;
load('digits.mat');

%Convert training and testing data into 2D
trainImages = Reshape(trainImages);
testImages = Reshape(testImages);

%calculate accuracy for the test data
eTestImages = testImages(:, 1:5000);
eTestLabels = testLabels(:, 1:5000);
hTestImages = testImages(:, 5000:end);
hTestLabels = testLabels(:, 5000:end);

%store the accuracy for easy and hard for both cosine and euclidean metric
eAccuracy1 = [];
hAccuracy1 = [];
eAccuracy2 = [];
hAccuracy2 = [];

%vary sample size
%for SampleSize = 1000:1000:60000
%for EigenSize = 10:10:500
    SampleSize = 35000;
    EigenSize = 700;
    %randomly select train data
    EigenData = datasample(trainImages, EigenSize, 2, 'Replace', false);
    
    %calculate Mean, Eigen Values and EigenVectors for the Covariance Matrix
    [Mean, ANorm, EVector, Evalue] = hw1FindEigendigits(EigenData);
    
    [trImages, index] = datasample(trainImages, SampleSize, 2, 'Replace', false);
    A = double(trImages);
    NImage = reshape(A(:, 1:10), 28, 28*10);
    imshow(NImage);
    imwrite(NImage,'Original Image.bmp','bmp');
    
    ANorm = bsxfun(@minus, A, Mean);
    
    MImage = reshape(ANorm(:, 1:10), 28, 28*10);
    imshow(MImage);
    imwrite(MImage,'Mean Image.bmp','bmp');
    
    B = ANorm;
    %for eSize = 1:1:size(EVector,2)
    eSize = 27;
    
    %transform test data in Eigen Coordinate frame
    ANorm  = double(B') * double(EVector(:,1:eSize));
    
    Rimages = EVector(:,1:eSize) * ANorm(1:1, :)';
    size(Rimages)
    Rimages = reshape(Rimages, 28, 28*1);
    imshow(Rimages);
    
    image = strcat('Rimages', num2str(eSize), '.bmp');
    imwrite(Rimages,image,'bmp');
    %for kNeighbor = 1:1:20
        kNeighbor = 7;
        
        %train model for cosine and euclidean distance metric
        model1 = fitcknn(ANorm, trainLabels(index), 'NumNeighbors', kNeighbor, 'Distance', 'cosine');
        model2 = fitcknn(ANorm, trainLabels(index), 'NumNeighbors', kNeighbor, 'Distance', 'euclidean');

        % randomly select test data
        testSampleCount = 1000;
        [eTestData, eIndex] = datasample(eTestImages, testSampleCount, 2, 'Replace', false);
        [hTestData, hIndex] = datasample(hTestImages, testSampleCount, 2, 'Replace', false);

        %calculate accuracy for the test data using model 1
        eAccuracy1 = [eAccuracy1; Test(eTestData, eTestLabels(eIndex), model1, Mean, EVector(:,1:eSize))];
        hAccuracy1 = [hAccuracy1; Test(hTestData, hTestLabels(hIndex), model1, Mean, EVector(:,1:eSize))];
        
        %calculate accuracy for the test data using model 2
        eAccuracy2 = [eAccuracy2; Test(eTestData, eTestLabels(eIndex), model2, Mean, EVector(:,1:eSize))];
        hAccuracy2 = [hAccuracy2; Test(hTestData, hTestLabels(hIndex), model2, Mean, EVector(:,1:eSize))];
        %end; %% Eigen Vector Number
    %end; %% Neighbor size
%end;  %% EigenSize End loop
%end; %% Sample Size End Loop

%{
%Plot for Accuracy vs neighbor size in KNN
plot([1:1:20], eAccuracy, 'r-*', [1:1:20], hAccuracy, 'b--o');
xlabel('Neighbor Size');
ylabel('Accuracy');
title('Accuracy Vs Neighbor Size');
legend('Easy Test Images', 'Hard Test Images');
grid on;
%}

%{
%% Plot for Accuracy VS Sample Size
plot([1000:1000:60000], eAccuracy2, 'r-*', [1000:1000:60000], hAccuracy2, 'b--o');
xlabel('Sample Size');
ylabel('Accuracy');
title('Accuracy Vs Sample Size');
legend('Easy Test Images', 'Hard Test Images');
grid on;
%}

%{ 
%% plot for Accuracy versus Eigen Vectors
plot([10:10:500], eAccuracy, 'r-*', [10:10:500], hAccuracy, 'b--o');
xlabel('Nunber of Eigen Vectors');
ylabel('Accuracy');
title('Accuracy Vs Eigen Vectors Number');
legend('Easy Test Images', 'Hard Test Images');
grid on;
%}

%{
%Plot for accuracy for cosing and euclidean distance metric
plot([1000:1000:60000], hAccuracy1, 'r-*', [1000:1000:60000], hAccuracy2, 'b--o');
xlabel('Sample Size');
ylabel('Accuracy');
title('Accuracy Vs Sample Size (Hard Dataset)');
legend('Cosine Distance', 'Euclidean Distance');
grid on;
%}

%{
plot([1000:1000:60000], eAccuracy2, 'r-*', [1000:1000:60000], hAccuracy2, 'b--o');
xlabel('Sample Size');
ylabel('Accuracy');
title('Accuracy Vs Sample Size (Euclidean)');
legend('Easy Test Images', 'Hard Test Images');
grid on;
%}

%{
%Plot for accuracy versus the number of eigen vectors 
%from all the eigen vectors calculated 
plot([1:1:260], eAccuracy2, 'r', [1:1:260], hAccuracy2, 'b');
xlabel('Eigen Vectors Number (260)');
ylabel('Accuracy');
title('Accuracy Vs Eigen Vectors Number(Euclidean)');
legend('Easy Test Images', 'Hard Test Images');
grid on;
%}