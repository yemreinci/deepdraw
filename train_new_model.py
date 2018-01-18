import sys
import pickle
from tensorflow import keras
import numpy as np

pickle_file = sys.argv[1]

with open(pickle_file, 'rb') as f:
    X, y = pickle.load(f)

perm = np.random.permutation(X.shape[0])
X = X[perm]
y = y[perm]

optimizer = keras.optimizers.Adam(lr=0.001)

model = keras.models.Sequential([
    keras.layers.Conv2D(8, input_shape=(32, 32, 1), kernel_size=(3, 3), strides=(1, 1), padding='same',
                        activation='relu'),
    keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same'),

    keras.layers.Conv2D(16, kernel_size=(3, 3), strides=(1, 1), padding='same',
                        activation='relu'),
    keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same'),

    keras.layers.Conv2D(32, kernel_size=(3, 3), strides=(1, 1), padding='same',
                        activation='relu'),
    keras.layers.MaxPool2D(pool_size=(3, 3), strides=(2, 2), padding='same'),

    keras.layers.Flatten(),

    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X, y, validation_split=0.2, batch_size=32, epochs=25, verbose=1).history

model.save('cnn_model.h5')