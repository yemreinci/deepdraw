import io
from base64 import b64decode
from scipy.misc import imread, imresize
from learning import graph, active_model
from web.models import Image
from tqdm import tqdm
import numpy as np
import pickle


def b64_to_np_array(data):
    file = io.BytesIO(b64decode(data))

    return np.expand_dims(imresize(imread(file, mode='L'), size=(32, 32)).astype(np.float32) / 255, axis=-1)


def predict(image):
    with graph.as_default():
        res = active_model.predict(np.array([image]))

    res = np.argmax(res)

    return res


def extract_data(fname):
    images = Image.objects.all()

    X = np.zeros((len(images), 32, 32, 1), dtype=np.float32)
    y = np.zeros((len(images), 10), dtype=np.float32)

    for i, image in tqdm(enumerate(images)):
        X[i, :, :] = b64_to_np_array(image.data)
        y[i, int(image.label)] = 1.0

    f = open(fname, 'wb')
    pickle.dump((X, y), f)