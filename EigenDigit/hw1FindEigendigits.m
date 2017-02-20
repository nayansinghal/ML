function [ Mean, ANorm,  V, D ] = 	hw1FindEigendigits( A )
%Calculate the Eigen Vectors for the Covariance Matrix
[r, c] = size(A);

A = double(A);
Mean =  mean(A,2);
%Subtract Mean from the matrix
ANorm = bsxfun(@minus, A, Mean);

%Calculate Covariance Matrix for A * A'
Covariance = (ANorm' * ANorm) .* (1/c);

%calculate Eigen Vectors for Covariance Matrix
[V, D] = eig(Covariance);

%Calculate Eigen Vectors for A' * A
V = ANorm * V;
%Sort Eigen Vectors with respect to Eigen Values in descending order
[D, indices] = sort(diag(D), 'descend');
V = V(:, indices);

% Display top n eigen vectors.
n = 20;
imshow(reshape(V(:,1:n), 28, 28*n));
t = title('Top 20 Eigen Vectors');
set(t, 'FontSize', 16);
imwrite(reshape(V(:,1:n), 28, 28*n),'Top 20 Eigen Vectors.png','png');

%normalize all the Eigen Vectors
V = normc(V);
end

