from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

CORS(app)

# LOAD MODEL
model = tf.keras.models.load_model(
    'models/plant_disease_model.keras'
)

# CLASS NAMES
# IMPORTANT:
# Replace these with YOUR actual dataset classes

class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# HOME ROUTE
@app.route('/')
def home():
    return "Plant Disease Backend Running in5 5000"


# PREDICTION ROUTE
@app.route('/predict', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return jsonify({
            'error': 'No file uploaded'
        })

    file = request.files['file']

    # OPEN IMAGE
    img = Image.open(file)

    # RGB CONVERSION
    img = img.convert('RGB')

    # RESIZE
    img = img.resize((256,256))

    # IMAGE → ARRAY
    img = np.array(img)

    # NORMALIZE
    img = img / 255.0

    # ADD BATCH DIMENSION
    img = np.expand_dims(img, axis=0)

    # PREDICT
    prediction = model.predict(img)

    predicted_class = class_names[np.argmax(prediction)]

    confidence = float(np.max(prediction))

    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
