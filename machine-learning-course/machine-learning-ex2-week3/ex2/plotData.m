function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure and hold
figure;
hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%

positive_indices = find(y==1);
negative_indices = find(y==0);

positive_mark_x = X(positive_indices,1);
positive_mark_y = X(positive_indices,2);
negative_mark_x = X(negative_indices,1);
negative_mark_y = X(negative_indices,2);

plot(positive_mark_x, positive_mark_y, 'k+', 'LineWidth', 2, 'MarkerSize', 7);
plot(negative_mark_x, negative_mark_y, 'ko', 'MarkerFaceColor', 'y', 'MarkerSize', 7);

% =========================================================================

#cancle hold
hold off;

end
