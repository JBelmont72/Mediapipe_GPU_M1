import tensorflow as tf
print("TensorFlow version:", tf.__version__)
devices = tf.config.list_physical_devices()
print("\nDevices: ", devices)
