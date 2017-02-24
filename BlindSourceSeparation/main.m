clear all;
clc;
close all;

for datasetSize = 44000:44000:44000
    load('sounds.mat');
    sounds = sounds(:,1:datasetSize);
    
    
    dataset = [1,2,3,4,5];
    for CombSize = 2:1:5
        Comb = combnk(dataset, CombSize);
        
        NumOfSignals = CombSize;
        NumOfSamples = CombSize;
        for row = 1:1:size(Comb,1)
            index = [];
            title = 0;
            for col = 1: 1: size(Comb, 2)
                index = [index, Comb(row, col)];
                title = title*10 + Comb(row, col);
            end; 
            U = sounds(index,:);
            %X = A*U;

            matrixError = [];
            [mixedSignals, A] = mixSignals(sounds, NumOfSignals, NumOfSamples, index);

            % Varying learning rate
            for learningRate = 0.01: 0.01:0.01
                % Varying number of iterations
                for numIters = 100000:100000:100000
                    error = 0;
                    % Varying count number
                    for count = 1:1:1

                        W = initMatrix( mixedSignals, NumOfSamples );
                        [Y,W] = ICA(learningRate, numIters, mixedSignals, W, NumOfSamples);
                        error = error + (norm(pinv(A) - W));

                    end; %% end count number
                    matrixError = [matrixError; error/10];
                    plotResults(U, mixedSignals, Y, title);
                    save(strcat(strcat('output/combination/Y_data_',num2str(title)),'.mat'), 'Y');
                end; % end NumIters
            end; %end Learning rate
        end; %end combination iteration
    end; %end combination number iteration
end; %end dataset size
%plot([100:100:10000], matrixError)
