import os
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json, re

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

# Dataset normalization
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

# Gemini Config
genai.configure(api_key="AIzaSyDGWDKsR3Rk5hdOLIfc0fY4WTEPPqiBipg")  # Replace with your actual key

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 512,
    }
)

# Gemini Severity Assessment
def get_gemini_assessment(hba1c, blood_pressure, duration, serum_creatinine, lipid_profile):
    prompt = f"""
These are the vitals of a diabetic patient:
- HbA1c: {hba1c} %
- Blood Pressure: {blood_pressure} mmHg
- Duration of Diabetes: {duration} years
- Serum Creatinine: {serum_creatinine} mg/dL
- Lipid Profile: {lipid_profile} mg/dL

Please assess the patient's condition severity on a scale from 1 to 10, where:
- 1 means the safest condition,
- 10 means the most critical condition.

Also include a short justification (within 50 words) for the assigned severity.

Return the output strictly in the following JSON format:
{{
  "severity_score": <number from 1 to 10>,
  "reason": "<concise explanation within 50 words>"
}}
    """

    try:
        response = gemini_model.generate_content([prompt])
        text = response.text
        json_string = re.search(r'\{.*\}', text, re.DOTALL)
        if json_string:
            return json.loads(json_string.group())
        else:
            return {
                "severity_score": None,
                "reason": "Unable to parse Gemini response"
            }
    except Exception as e:
        print("Gemini API error:", e)
        return {
            "severity_score": None,
            "reason": "Gemini API call failed"
        }

def print_patient_vitals(hba1c, blood_pressure, duration, serum_creatinine, lipid_profile, predicted_class, severity_data):
    print("=== Patient Vitals and Diagnosis ===")
    print(f"HbA1c: {hba1c} %")
    print(f"Blood Pressure: {blood_pressure} mmHg")
    print(f"Duration of Diabetes: {duration} years")
    print(f"Serum Creatinine: {serum_creatinine} mg/dL")
    print(f"Lipid Profile: {lipid_profile} mg/dL")
    print(f"Predicted Retinopathy Class: {predicted_class}")
    print("=== Gemini Assessment ===")
    print(f"Severity Score: {severity_data.get('severity_score')}")
    print(f"Reason: {severity_data.get('reason')}")
