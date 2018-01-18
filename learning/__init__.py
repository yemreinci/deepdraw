import tensorflow as tf
from tensorflow import keras

graph = tf.Graph()
active_model = None

with graph.as_default():
    active_model = keras.models.load_model('cnn_model.h5')
