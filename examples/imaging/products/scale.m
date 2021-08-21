function [X] = scale(X, sf, st)
%SCALE Summary of this function goes here
%   Detailed explanation goes here

EPS = 1.0e-16;

a = sf(1) + 0.0;
b = sf(2) + 0.0;
c = st(1) + 0.0;
d = st(2) + 0.0;

X(X < a) = a;
X(X > b) = b;

X = (X - a) * (d - c) / (b - a + EPS) + c;
end

