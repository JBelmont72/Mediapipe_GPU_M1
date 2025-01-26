''' this program will analyze hand positions
https://keras.io/api/datasets/mnist/
to load 60,000 sets of 10 digits
keras.datasets.mnist.load_data(path="mnist.npz")
https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz

tutorial Must read  https://www.tensorflow.org/tutorials/keras/classification

'''



import tensorflow as tf
from future import absolute_import, division, print_function, unicode_literals
print("TensorFlow version:", tf.__version__)
devices = tf.config.list_physical_devices()
print("\nDevices: ", devices)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  details = tf.config.experimental.get_device_details(gpus[0])
  print("GPU details: ", details)
###You can verify that TensorFlow will utilize the GPU 
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
# test the performance gain with the following script. Run this script once with GPU (metal) support enabled and once in a virtual environment without metal installed.
# mnist = tf.keras.datasets.mnist

# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
tf.keras.layers.Flatten(input_shape=(28, 28)),
tf.keras.layers.Dense(128, activation='relu'),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
loss='sparse_categorical_crossentropy',
metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test, y_test, verbose=2)