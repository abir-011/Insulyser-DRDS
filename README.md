# Insulyser - Diabetic Retinopathy Detection System Ver.2

This repository contains a web application built using Django and HTML/CSS for detecting different stages of diabetic retinopathy from retinal images. 
The application allows users to upload scanned retinal images and provides predictions on the stage of diabetic retinopathy, including mild, moderate, no diabetic retinopathy, proliferative diabetic retinopathy, and severe diabetic retinopathy.
It now combines our CNN model's prediction and a generative AI (Gemini) system to provide a comprehensive severity assessment and final diagnosis based on other essential body factors too such as hba1c, blood_pressure, duration, serum_creatinine and lipid_profile.

[For version 1 click here](https://github.com/saurav6422/Diabetic-Retinopathy-Detection-System)

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Team](#team)

## Features

- User authentication: Secure login page to access the application.
- Image upload: Users can upload scanned retinal images for analysis.
- Diabetic retinopathy prediction: The application utilizes a pre-trained model to predict the stage of diabetic retinopathy based on the uploaded image.
- Result display: The application displays the predicted stage of diabetic retinopathy along with relevant information and recommendations.
- About and contact pages: Additional pages provide information about the application and contact details.

## Requirements

- Python 3.7+
- Django 5.0
- TensorFlow / Keras
- [requirements.txt](requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abir-011/Insulyser-DRDS.git
   cd Insulyser-DRDS
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations and create the database:

   ```bash
   python manage.py migrate
   ```

## Usage

1. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

2. Open your browser and go to http://localhost:8000 to access the application.
3. Log in to the application using the provided credentials.
4. Navigate to the home page and click the "Upload Image" button.
5. Select a scanned retinal image from your local filesystem.
6. Wait for the application to process the image and display the predicted stage of diabetic retinopathy.
7. Follow the provided recommendations or seek medical advice based on the prediction.

## File Structure

- `drds_project/` : Django project root.
- `drds_project/urls.py` : Project-level URL routing.
- `drds_app/` : Main app handling all backend logic and routing.
- `drds_app/urls.py` : App-level URL routing.
- `model/` : Contains the trained model file `model_2.h5`.
- `templates/` : HTML templates for frontend rendering.
- `views.py` : Core logic for image processing and prediction.
- `utils.py` – Helper functions now also includes Gen-AI integration.
- `media/` : Stores uploaded images.
- `dataset/` – Dataset used for training.
- `requirements.txt` – List of required Python packages.
- `manage.py` – Django project entry point.

## License

This project is licensed under the GNU General Public License v2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [OpenCV](https://opencv.org/)
- [Keras](https://keras.io/)
- [TenserFlow](https://www.tensorflow.org/)
- [Git LFS – For handling the large model file](https://git-lfs.com/)

## Team

- Aditya - Machine Learning Engineer - [Git](https://github.com/Aditya-039)
- Saurav - Machine Learning Engineer | Backend Developer - [Git](https://github.com/saurav6422)
- Sambarta - Frontend Developer - [Git](https://github.com/Sambarta-2001)
- Abir - Backend Developer | Machine Learning Engineer - [Git](https://github.com/abir-011)
