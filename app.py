
from flask import Flask, request, render_template, jsonify # Added jsonify
import joblib
from feature_extraction import extract_features_from_url
import os
from flask_cors import CORS # For allowing requests from the extension

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Ensure these files are in the same directory as app.py or provide correct paths
# and that they are included in your Render deployment.
try:
    model = joblib.load('phishing_rf_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError as e:
    print(f"ERROR: Model or scaler file not found. Make sure 'phishing_rf_model.pkl' and 'scaler.pkl' are present.")
    print(e)
    # Depending on your Render setup, you might want to exit or handle this gracefully.
    # For now, the app will likely crash if these aren't found at startup.
    raise

@app.route('/')
def index():
    return render_template('index.html')

# Existing route for HTML response (for your web page)
@app.route('/predict', methods=['POST'])
def predict_html(): # Renamed to avoid conflict, though not strictly necessary with different logic
    url = request.form['url']
    features_df = extract_features_from_url(url) # Assuming extract_features_from_url returns a DataFrame

    if features_df is None or features_df.empty:
        result = "Error: Could not extract features. Assuming Legitimate ✅"
        return render_template('index.html', prediction=result, url=url)

    try:
        features_scaled = scaler.transform(features_df)
        prediction = model.predict(features_scaled)
        # model.predict returns an array, e.g. [1] or [0]
        result = "Phishing Website 🚨" if prediction[0] == 1 else "Legitimate Website ✅"
    except Exception as e:
        print(f"Error during HTML prediction for {url}: {e}")
        result = "Error during prediction. Assuming Legitimate ✅" # Fail safe
    return render_template('index.html', prediction=result, url=url)

# New API route for JSON response (for the extension)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    # Check if request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON", "is_phishing": False}), 415 # 415 Unsupported Media Type

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided in JSON body", "is_phishing": False}), 400

    url_to_check = data['url']
    if not url_to_check: # Check for empty URL string
        return jsonify({"error": "URL cannot be empty", "is_phishing": False}), 400

    print(f"API: Received URL for prediction: {url_to_check}") # For Render logs

    features_df = extract_features_from_url(url_to_check)

    if features_df is None or features_df.empty:
        print(f"API: Feature extraction failed for {url_to_check}")
        return jsonify({
            "message": "Feature extraction failed",
            "is_phishing": False, # Fail safe: assume not phishing if features can't be extracted
            "prediction_value": 0,
            "url": url_to_check
        })

    try:
        features_scaled = scaler.transform(features_df)
        prediction = model.predict(features_scaled) # prediction is likely numpy array, e.g., array([0])
        prediction_value = int(prediction[0])
        is_phishing_bool = bool(prediction_value == 1)

        print(f"API: Prediction for {url_to_check}: {'Phishing' if is_phishing_bool else 'Legitimate'} (Value: {prediction_value})")
        return jsonify({
            "is_phishing": is_phishing_bool,
            "prediction_value": prediction_value,
            "url": url_to_check
        })
    except Exception as e:
        print(f"Error during API prediction for {url_to_check}: {e}")
        # Fail safe in case of prediction error
        return jsonify({
            "error": f"Prediction error: {str(e)}",
            "is_phishing": False,
            "prediction_value": 0,
            "url": url_to_check
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) # Render sets the PORT environment variable
    app.run(host="0.0.0.0", port=port)
