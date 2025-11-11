# Plagiarism Checker API using Cosine Similarity + ML

This project implements a plagiarism detection system using text similarity (Cosine Similarity) and an ML classifier (Logistic Regression). It provides both a Flask API backend and a Streamlit frontend, and uses Kong for API Gateway rate and size limiting.

---

## 🧰 Tech Stack

- **Language:** Python 3.11+
- **Backend:** Flask
- **Frontend:** Streamlit
- **ML Model:** Logistic Regression (scikit-learn)
- **Vectorization:** TF-IDF
- **Similarity:** Cosine Similarity
- **API Gateway:** Kong (Rate limiting & Request size limiting)
- **Utilities:** NumPy, pandas, joblib, difflib

---

## 📁 Project Structure

```
plagiarism_checker/
│
├── flask_api/
│   ├── app.py                 # Flask API
│   ├── utils.py               # Helper functions (similarity, highlighting)
│   ├── model.py               # Train & save ML model
│   └── plagiarism_model.pkl   # Trained ML model
│
├── streamlit_app/
│   └── app.py                 # Streamlit frontend
│
├── rate_limit_algorithms/
│   └── token_leaky_bucket.py  # Token Bucket & Leaky Bucket implementation
│
├── sample_data/
│   ├── original.txt
│   └── submission.txt
│
├── requirements.txt
└── README.md
```

## ⚡ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd plagiarism_checker
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🏗️ Backend - Flask API

#### Train ML Model
```bash
python flask_api/model.py
```

#### Run Flask API
```bash
python flask_api/app.py
```
Endpoint: POST http://localhost:5000/check
Request: Multipart; keys: original, submission

### 🎨 Frontend - Streamlit App
```bash
streamlit run streamlit_app/app.py
```
- Upload original and submitted text files
- Displays cosine similarity, probability, and highlighted matches

### 🔧 Kong API Gateway Setup (Optional)
Create Service & Route:
```bash
curl -i -X POST http://localhost:9001/services --data "name=plagiarism-api" --data "url=http://localhost:5000"
curl -i -X POST http://localhost:9001/services/plagiarism-api/routes --data "paths[]=/check"
```
Enable Rate Limiting:
```bash
curl -i -X POST http://localhost:9001/services/plagiarism-api/plugins --data "name=rate-limiting" --data "config.minute=5" --data "config.policy=local"
```
Enable Request Size Limiting:
```bash
curl -i -X POST http://localhost:9001/services/plagiarism-api/plugins --data "name=request-size-limiting" --data "config.allowed_payload_size=1024"
```

### 🏋️ Rate Limiting Algorithms

Implemented Token Bucket and Leaky Bucket algorithms for demonstration:
```bash
python rate_limit_algorithms/token_leaky_bucket.py
```
- Shows allowed/rejected requests per algorithm
- Extendable to API request throttling

## 📄 Assignment Deliverables

Screenshots for:
- Streamlit App with uploaded files
- Cosine similarity & plagiarism results
- Highlighted matching text
- Rate limiting in action (Kong)

Code:
- Flask API, Streamlit frontend, ML model, utils, rate limiting algorithms
- requirements.txt for environment setup

## 📌 Notes

- Do not commit venv/ folder. Use requirements.txt for recreating environment.
- Sample data is available in sample_data/.
- Kong API Gateway config is optional locally but required for assignment completeness.
