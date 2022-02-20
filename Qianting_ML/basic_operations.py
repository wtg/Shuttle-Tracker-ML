#%%
from __future__ import print_function
import tensorflow as tf

# Define tensor constants.
a = tf.constant(2)
b = tf.constant(3)
c = tf.constant(5)

# Various tensor operations.
# Note: Tensors also support python operators (+, *, ...)
add = tf.add(a, b)
sub = tf.subtract(a, b)
mul = tf.multiply(a, b)
div = tf.divide(a, b)

# Access tensors value.
print("add =", add.numpy())
print("sub =", sub.numpy())
print("mul =", mul.numpy())
print("div =", div.numpy())

# Some more operations.
mean = tf.reduce_mean([a, b, c])
sum = tf.reduce_sum([a, b, c])

# Access tensors value.
print("\n")
print("mean =", mean.numpy())
print("sum =", sum.numpy())

# Matrix multiplications.
matrix1 = tf.constant([[1., 2.], [3., 4.]])
matrix2 = tf.constant([[5., 6.], [7., 8.]])

product = tf.matmul(matrix1, matrix2)
# Display Tensor.
print("\n")
print(product)


# Convert Tensor to Numpy.
print("\n")
print(product.numpy())
# %%
