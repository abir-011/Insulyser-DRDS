import os
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

# Model Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'drds_app', 'model', 'model_2.h5')
model = load_model(MODEL_PATH)

class_labels = ['Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe']

# Image Preprocessing
def preprocess_image(img):
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_YCrCb = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2YCrCb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
    img_YCrCb[:, :, 0] = clahe.apply(img_YCrCb[:, :, 0])
    img_RGB_2 = cv2.cvtColor(img_YCrCb, cv2.COLOR_YCrCb2RGB)
    img_blur = cv2.GaussianBlur(img_RGB_2, (5, 5), 0)
    return img_blur

# Data normalization
data_dir = os.path.join(BASE_DIR, 'dataset', 'train')
clases = sorted(os.listdir(data_dir))
x_train = np.array([
    preprocess_image(cv2.imread(os.path.join(data_dir, cl, name)))
    for cl in clases for name in os.listdir(os.path.join(data_dir, cl))
])
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    validation_split=0.2
)
datagen.fit(x_train)

# Prediction
def predict_class(image_path):
    try:
        img = cv2.imread(image_path)
        preprocessed = preprocess_image(img)
        x_test = np.expand_dims(preprocessed, axis=0)
        x_test = (x_test - datagen.mean) / (datagen.std + 1e-6)
        predictions = model.predict(x_test)
        index = predictions.argmax(axis=-1)[0]
        return class_labels[index]
    except Exception as e:
        print("Prediction error:", e)
        return None
