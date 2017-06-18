function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

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

constant = 1/m;
constant_regularization = lambda/(2*m);
constant_reg_grad = lambda/m;

linear_prediction = X*theta;
prediction = sigmoid(linear_prediction);

%find cost
cost_positive = -1 * (y'*(log(prediction)));
cost_negative = -1 * ((1 .- y)'*(1 .- log(prediction)));
cost_regularization = constant_regularization*sum(theta(2:end,1) .^ 2);
J = constant*(cost_positive + cost_negative) + cost_regularization;

%find gradient
grad = constant*( X'*(prediction .- y)) .+ constant_reg_grad*theta;
grad(1) -= constant_reg_grad*theta(1);

% =============================================================

end
