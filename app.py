from flask import Flask, request, render_template
import joblib
from feature_extraction import extract_features_from_url
import os
app = Flask(__name__)

model = joblib.load('phishing_rf_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    features = extract_features_from_url(url)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    result = "Phishing Website 🚨" if prediction == 1 else "Legitimate Website ✅"
    return render_template('index.html', prediction=result, url=url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
