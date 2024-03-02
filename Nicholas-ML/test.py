import tensorflow as tf
import numpy as np
import random

# Define the input layers
input1 = tf.keras.layers.Input(shape=(1,), name='input1')
input2 = tf.keras.layers.Input(shape=(1,), name='input2')

# Concatenate the inputs
concatenated_inputs = tf.keras.layers.Concatenate()([input1, input2])

# Define some hidden layers
hidden1 = tf.keras.layers.Dense(32, activation='relu')(concatenated_inputs)
hidden2 = tf.keras.layers.Dense(16, activation='relu')(hidden1)

# Define the output layers
output1 = tf.keras.layers.Dense(1, name='output1')(hidden2)
output2 = tf.keras.layers.Dense(1, name='output2')(hidden2)

# Create the model
model = tf.keras.models.Model(inputs=[input1, input2], outputs=[output1, output2])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Print the model summary
model.summary()

# Define the inputs and outputs
input_data1 = []
input_data2 = []
output_data1 = []
output_data2 = []
for i in range(1000):
    random_number = random.randint(1, 10)
    input_data1.append(random_number)
    output_data1.append(random_number*2)
for j in range(1000):
    random_number = random.randint(1, 10)
    input_data2.append(random_number)
    output_data2.append(random_number*random_number)
input_data1 = np.array(input_data1)
input_data2 = np.array(input_data2)
output_data1 = np.array(output_data1)
output_data2 = np.array(output_data2)
# input_data1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# input_data2 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 1, 1, 1])
# output_data1 = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
# output_data2 = np.array([0, 1, 4, 9, 16, 25, 36, 49, 1, 1, 1])

# Reshape inputs for TensorFlow
input_data1 = input_data1.reshape(-1, 1)
input_data2 = input_data2.reshape(-1, 1)

# Normalize outputs
output_data1_normalized = output_data1 / 8.0  # Normalize by dividing by the maximum value in output1
output_data2_normalized = output_data2 / 16.0  # Normalize by dividing by the maximum value in output2

# Train the model
model.fit(x=[input_data1, input_data2], y=[output_data1_normalized, output_data2_normalized], epochs=1000, verbose=1)

# Test the model
test_input_data1 = np.array([4])
test_input_data2 = np.array([5])
test_input_data1 = test_input_data1.reshape(-1, 1)
test_input_data2 = test_input_data2.reshape(-1, 1)
predictions = model.predict([test_input_data1, test_input_data2])
print("Predicted Output 1:", predictions[0] * 8.0)  # De-normalize output1 prediction
print("Predicted Output 2:", predictions[1] * 16.0)  # De-normalize output2 prediction
