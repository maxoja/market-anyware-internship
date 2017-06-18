function [J, grad] = costFunction(theta, X, y)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%

constant = 1/m;
linear_prediction = X*theta; %column vector
discrete_prediction = sigmoid(linear_prediction); %column vector

%start calculating cost
case_positive_cost = -1 .* (y'*log(discrete_prediction)); %scalar
case_negative_cost = -1 .* ((1 .- y)'*log(1 .- discrete_prediction)); %scalar

J = constant*(case_positive_cost + case_negative_cost);

%start calculating gradient
prediction_error = discrete_prediction - y; %column vector
grad = constant .* (X'*prediction_error);

% =============================================================

end
