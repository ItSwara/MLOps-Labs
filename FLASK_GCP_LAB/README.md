# 🐧 Antarctic Penguin Species Classifier

A machine learning web application that classifies Palmer Archipelago penguin species using an SVM model, served via a Flask API and visualized through a Streamlit frontend.

---

## 📁 Project Structure

```
/
├── Dockerfile           – Docker image for the Flask prediction API
├── README.md            – Project overview and setup instructions
├── requirements.txt     – Python dependencies
├── streamlit_app.py     – Streamlit frontend (runs locally)
├── model/
│   └── svm_model.pkl    – Trained SVM model + scaler
└── src/
    ├── data/
    │   └── penguins.csv – Palmer Penguins dataset
    ├── main.py          – Flask API with /predict endpoint
    ├── predict.py       – Model loading and prediction logic
    ├── test_api.py      – Integration tests for the Flask API
    └── train.py         – Model training and saving script
```

---

## 🧠 Model

- **Algorithm**: Support Vector Machine (SVM) with RBF kernel
- **Dataset**: Palmer Penguins (344 rows, 333 after null removal)
- **Target**: Species — Adelie, Chinstrap, Gentoo
- **Accuracy**: 100% on test set (67 samples, stratified split)

**Features used:**

| Feature | Type |
|---|---|
| `island` | Categorical (encoded) |
| `bill_length_mm` | Numeric |
| `bill_depth_mm` | Numeric |
| `flipper_length_mm` | Numeric |
| `body_mass_g` | Numeric |
| `sex` | Categorical (encoded) |

---

## 🚀 Setup & Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python src/train.py
```

### 3. Run the Flask API
```bash
python src/main.py
```

### 4. Test the API
```bash
python src/test_api.py
```

Or with curl:
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"bill_length_mm": 39.1, "bill_depth_mm": 18.7, "flipper_length_mm": 181.0, "body_mass_g": 3750, "island": "Torgersen", "sex": "Male"}'
```

### 5. Run the Streamlit frontend
```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deployment (Google Cloud Run)

### Build & push image
```bash
gcloud builds submit --tag gcr.io/[YOUR_PROJ_ID]/penguin-app
```

### Deploy to Cloud Run
```bash
gcloud run deploy penguin-app \
  --image gcr.io/[YOUR_PROJ_ID]/penguin-app \
  --platform managed \
  --port 8080 \
  --allow-unauthenticated
```

### Update Streamlit with deployed URL
In `streamlit_app.py`, replace:
```python
'http://127.0.0.1:8080/predict'
```
with your Cloud Run URL, then run:
```bash
streamlit run streamlit_app.py
```

### Delete a Cloud Run service
```bash
gcloud run services delete [SERVICE_NAME] --region [REGION]
```

---

## 🧪 Sample Test Values

| Species | Bill Length | Bill Depth | Flipper | Mass | Island | Sex |
|---|---|---|---|---|---|---|
| Adelie | 39.1 | 18.7 | 181.0 | 3750 | Torgersen | Male |
| Chinstrap | 46.5 | 17.9 | 192.0 | 3500 | Dream | Female |
| Gentoo | 47.5 | 14.8 | 218.0 | 5700 | Biscoe | Male |

---

## 🛠️ Built With

- [scikit-learn](https://scikit-learn.org/) — SVM model
- [Flask](https://flask.palletsprojects.com/) — REST API
- [Streamlit](https://streamlit.io/) — Frontend UI
- [Google Cloud Run](https://cloud.google.com/run) — Deployment
