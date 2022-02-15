from __future__ import absolute_import, division, print_function

from tkinter import Y
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

csv_file = open('Data_session.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter = ',')

csv_list = list(csv_reader)

id = '85'
session = 5
x_train = []
y_train = []


for line in csv_list:
    if line[0] == id and int(line[5]) <= session:
        x_train.append(line[1])
        y_train.append(line[2])
        #print(x_train)





rng = np.random

learning_rate = 0.01
training_steps = 3000
display_steps = 50
##################
X = np.array(x_train)
Y = np.array(y_train)

W = tf.Variable(rng.randn(), name = "weight")
b = tf.Variable(rng.randn(), name = "bias")

def linear_regression(x):
    return tf.add(tf.multiply(W, x), b) # Wx + b


def mean_square(y_pred, y_true):
    return tf.reduce_mean(tf.square(y_pred - y_true))

optimizer = tf.optimizers.SGD(learning_rate) # gradient descent optimizer

# optimization process

def run_optimization():
    # gradientTape for automatic differentiation/rate of change
    with tf.GradientTape() as g:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)

    # compute gradient
    gradients = g.gradient(loss, [W, b])

    # Update W and b following gradient
    optimizer.apply_gradients(zip(gradients, [W, b]))


# Run training for the given number of steps
for step in range(1, training_steps + 1):
    run_optimization()

    if step % display_steps == 0:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)
       # print("step: %i, loss: %f, W: %f, b: %f" % (step, loss, W.numpy(), b.numpy()))

plt.plot(X, Y, 'ro', label='Original data')
plt.plot(X, np.array(W * X + b), label='Fitted line')
plt.legend()
plt.show()