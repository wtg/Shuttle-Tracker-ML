import tensorflow as tf
import numpy as np

class CustomOptimizer(tf.keras.optimizers.Optimizer):
    def __init__(self, learningRate, name="CustomOptimizer", **kwargs):
        super(CustomOptimizer, self).__init__(name, **kwargs)
        self.learningRate = learningRate

    def get_config(self):
        config = super(CustomOptimizer, self).get_config()
        config.update({"learningRate": self.learningRate})
        return config

    def apply_gradients(self, grads_and_vars, name=None):
        updates = []
        for grad, var in grads_and_vars:
            if grad is None or var is None:
                continue
            new_var = var - self.learningRate * grad
            updates.append(var.assign(new_var))
        print(updates)
        return tf.group(*updates, name=name)

# Define the model
model = tf.keras.Sequential([tf.keras.layers.Dense(units=1, input_shape=[1])])

# Create an instance of the custom optimizer
custom_optimizer = CustomOptimizer(learningRate=0.001)

# Compile the model with the custom optimizer
model.compile(optimizer=custom_optimizer, loss='mean_squared_error')

# Training data
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)

# Train the model
model.fit(xs, ys, epochs=2)

# Make a prediction
print(model.predict([10.0]))