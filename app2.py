import os
import numpy as np
import librosa
import pickle
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask import flash, redirect
import warnings
warnings.filterwarnings('ignore')


UPLOAD_FOLDER = os.path.abspath("static/uploads")
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Load trained MLP Classifier model from file
with open('mlp_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# Load trained SVM model from file
with open('svm_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)

# Function to extract features from each audio file
def extract_features(file_path):
    audio, sampling_rate = librosa.load(file_path, sr=22050, duration=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sampling_rate, n_mfcc=30)
    features = np.mean(mfccs.T, axis=0)
    return features


def predict_rf(file_path):
    features = extract_features(file_path)
    prediction = rf_model.predict([features])[0]
    return prediction
def predict_svm(file_path):
    features = extract_features(file_path)
    prediction = svm_model.predict([features])[0]
    return prediction




@app.route('/')
def home():
    return render_template('Index-Final.html')


@app.route('/predict_voice', methods=['POST'])
def predict_voice():
    # Your code for handling voice (.wav) files and predictions
    # Example:
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(file_path)
    result_rf = predict_rf(file_path)
    result_svm = predict_svm(file_path)
    os.remove(file_path)

    return render_template('result-voice.html', result_rf=result_rf, result_svm=result_svm)

if __name__ == '__main__':
    app.run(debug=True)

