#!/usr/bin/env python
# encoding: utf-8
"""
NOTE: the operators + - * / are element wise operation. If you want
matrix multiplication use dot or mdot!
"""
from __future__ import print_function
import numpy as np
from numpy import dot
from numpy.linalg import inv
from numpy.linalg import multi_dot as mdot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sys import argv

# choose λ
###############################################################################

"""for e in range(9):
    exponent = e-3
    λ = 10**exponent
    
    print (λ)"""
λ = 25

# 3D plotting
###############################################################################
# Helper functions
def prepend_one(X):
    """prepend a one vector to X."""
    return np.column_stack([np.ones(X.shape[0]), X])

def grid2d(start, end, num=50):
    """Create an 2D array where each row is a 2D coordinate.
    np.meshgrid is pretty annoying!
    """
    dom = np.linspace(start, end, num)
    X0, X1 = np.meshgrid(dom, dom)
    return np.column_stack([X0.flatten(), X1.flatten()])
# a)
def squared_error(X, beta, y):
    #return dot(dot(X, beta)-y).T, dot((X, beta) -y)
    return dot((dot(X, beta)-y).T, dot(X, beta)-y)

"""# b)
def quadratic_features(matrix):
    dimensions = matrix.shape[0]
    print("Computing quadratic features for matrix with ", dimensions, "dimensions")
    d = matrix.shape[1]
    new_d = int(d + ((d* (d+1)) /2))"""
    
    
###############################################################################
# get regularization_parameter
print(argv)
#reg_par = int(argv[1])
reg_par = λ

# load the data
#data = np.loadtxt("dataLinReg2D.txt")
data = np.loadtxt("dataLinReg2D.txt")
print("data.shape:", data.shape)

# split into features and labels
X, y = data[:, :2], data[:, 2]
print("X.shape:", X.shape)
print("y.shape:", y.shape)

# 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # the projection arg is important!
ax.scatter(X[:, 0], X[:, 1], y, color="red")
ax.set_title("raw data")
plt.draw()

# show, use plt.show() for blocking
# prep for linear reg.
X = prepend_one(X)
print("X.shape:", X.shape)

# Fit model/compute optimal parameters beta
beta_ = mdot([inv(dot(X.T, X)), X.T, y])

###############################################################################
# a) include ridge regularization
    
print("Reg param", reg_par)
dimension = X.shape[1]
identity = np.eye(dimension, dtype = int)
identity[0][0] = 0 #that's beta_1 and usually not regularized

# Compute optimal coeffiecient beta
beta_ = mdot([inv(dot(X.T, X) + reg_par * identity), X.T, y])

# Squared Error
l = squared_error(X, beta_, y)
print("squared error: ", l) 

#print(identity)

print("Optimal beta:", beta_)
# prep for prediction
X_grid = prepend_one(grid2d(-3, 3, num=30))
print("X_grid.shape:", X_grid.shape)
# Predict with trained model
y_grid = dot(X_grid, beta_)
print("Y_grid.shape", y_grid.shape)

# vis the result
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # the projection part is important
ax.scatter(X_grid[:, 1], X_grid[:, 2], y_grid) # dont use the 1 infront
ax.scatter(X[:, 1], X[:, 2], y, color="red") # also show the real data
ax.set_title("predicted data")
plt.show()
