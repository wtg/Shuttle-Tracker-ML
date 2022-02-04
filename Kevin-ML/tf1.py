import tensorflow as tf
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

print("TensorFlow version:", tf.__version__)
#print(tf.config.list_physical_devices('GPU'))

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train/255.0, x_test/255.0
print("X_Train [0]: ", x_train[0])
print("Y_Train: ", y_train)


model = tf.keras.models.Sequential([\
        tf.keras.layers.Flatten(input_shape=(28,28)),\
        tf.keras.layers.Dense(128, activation='relu'),\
        tf.keras.layers.Dropout(0.2),\
        tf.keras.layers.Dense(10)])

predictions = model(x_train[:1]).numpy()
print("Prediction: ", predictions)

sMax = tf.nn.softmax(predictions).numpy()
print("Softmax predictions: ", sMax)

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

lossOut = loss_fn(y_train[:1], predictions).numpy()
print("Loss functions output: ", lossOut)

model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test, verbose=2)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
print(probability_model(x_test[:5]))
