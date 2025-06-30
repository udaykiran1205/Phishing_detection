
# 🛡️ Phishing Website Detection using Random Forest

This project uses a machine learning model (Random Forest Classifier) to detect phishing websites based on URL features. The model was trained and evaluated on a dataset containing labeled examples of phishing and legitimate websites.

## 🚀 Features

- Extracts lexical and domain-based features from URLs
- Trained using Random Forest algorithm
- PCA (Principal Component Analysis) applied to reduce dimensionality
- Flask-based UI for real-time prediction
- Deployment-ready for platforms like Render, Heroku, or Railway

---

## 🧠 Model Overview

- **Model**: Random Forest Classifier
- **Feature Engineering**: URL length, IP usage, special characters, domain info, etc.
- **Dimensionality Reduction**: PCA applied for improved performance
- **Evaluation Metrics**: Accuracy, Precision, Recall, Confusion Matrix

---

## 📁 Project Structure

```
phishing-detector/
├── app.py                     # Flask backend
├── phishing_rf_model.pkl      # Trained Random Forest model
├── scaler.pkl                 # Scaler used for feature normalization
├── requirements.txt           # Dependencies
├── templates/
│   └── index.html             # Frontend HTML page
└── static/
    └── style.css              # (optional) Styling
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/udaykiran1205/Phishing_detection.git
cd phishing-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Flask App Locally

```bash
python app.py
```

Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🌐 Deployment Options

### ✅ Deploy to Render

1. Push this repo to GitHub
2. Go to [https://render.com](https://render.com)
3. Click "New Web Service" → Connect your GitHub repo
4. Use:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python app.py`

The deployed link is --
# https://phishing-detection1.onrender.com/

### 🔁 Other Platforms

- Heroku (needs `Procfile`)
- Railway
- PythonAnywhere

---

## ✍️ Author

- **Your Name**
- [GitHub](https://github.com/udaykiran1205/Phishing_detection.git)

---

## 📜 License

This project is licensed under the MIT License.
