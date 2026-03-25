from flask import Flask, request, jsonify
from google.cloud import storage, bigquery
import os
import json
import datetime

app = Flask(__name__)

BUCKET_NAME = os.environ.get("BUCKET_NAME")


def get_bucket():
    storage_client = storage.Client()
    return storage_client.bucket(BUCKET_NAME)


def diabetes_risk_model(patient):
    pregnancies = float(patient.get("pregnancies", 0))
    glucose = float(patient.get("glucose", 0))
    blood_pressure = float(patient.get("blood_pressure", 0))
    skin_thickness = float(patient.get("skin_thickness", 0))
    insulin = float(patient.get("insulin", 0))
    bmi = float(patient.get("bmi", 0))
    diabetes_pedigree = float(patient.get("diabetes_pedigree", 0))
    age = float(patient.get("age", 0))

    raw_score = (
        0.03 * pregnancies
        + 0.02 * glucose
        + 0.01 * blood_pressure
        + 0.005 * skin_thickness
        + 0.002 * insulin
        + 0.04 * bmi
        + 0.5 * diabetes_pedigree
        + 0.03 * age
    )

    normalized_score = min(raw_score / 10.0, 1.0)

    if normalized_score >= 0.7:
        label = "High diabetes risk"
    elif normalized_score >= 0.4:
        label = "Moderate diabetes risk"
    else:
        label = "Low diabetes risk"

    return round(normalized_score, 4), label


def upload_json_to_gcs(folder_name, file_prefix, payload):
    bucket = get_bucket()
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    blob_name = f"{folder_name}/{file_prefix}_{timestamp}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        json.dumps(payload, indent=2),
        content_type="application/json"
    )
    return blob_name


@app.route("/")
def home():
    return "Diabetes ML pipeline service running"


@app.route("/upload-dataset", methods=["POST"])
def upload_dataset():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain dataset JSON"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Dataset must be a list of patient records"}), 400

    blob_name = upload_json_to_gcs("datasets", "diabetes_dataset", data)

    return jsonify({
        "message": "Dataset uploaded successfully",
        "record_count": len(data),
        "file": blob_name
    })


@app.route("/predict", methods=["POST"])
def predict():
    patient = request.get_json()

    if not patient:
        return jsonify({"error": "Request body must contain patient JSON"}), 400

    score, label = diabetes_risk_model(patient)

    result = {
        "input": patient,
        "risk_score": score,
        "prediction": label,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    blob_name = upload_json_to_gcs("predictions", "single_prediction", result)
    result["stored_file"] = blob_name

    return jsonify(result)


@app.route("/batch-predict", methods=["POST"])
def batch_predict():
    patients = request.get_json()

    if not patients:
        return jsonify({"error": "Request body must contain a list of patients"}), 400

    if not isinstance(patients, list):
        return jsonify({"error": "Batch input must be a list"}), 400

    predictions = []
    high_risk_count = 0

    for index, patient in enumerate(patients):
        score, label = diabetes_risk_model(patient)

        if label == "High diabetes risk":
            high_risk_count += 1

        predictions.append({
            "patient_index": index,
            "input": patient,
            "risk_score": score,
            "prediction": label
        })

    result = {
        "total_records": len(patients),
        "high_risk_count": high_risk_count,
        "predictions": predictions,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    blob_name = upload_json_to_gcs("predictions", "batch_prediction", result)
    result["stored_file"] = blob_name

    return jsonify(result)


@app.route("/artifacts", methods=["GET"])
def list_artifacts():
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(BUCKET_NAME)

    files = []
    for blob in blobs:
        files.append(blob.name)

    return jsonify({
        "bucket": BUCKET_NAME,
        "file_count": len(files),
        "files": files
    })


@app.route("/analytics", methods=["GET"])
def analytics():
    client = bigquery.Client()

    query = """
        SELECT name, SUM(number) AS total
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = 'CA'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 5
    """

    query_job = client.query(query)
    results = query_job.result()

    names = []
    for row in results:
        names.append({
            "name": row.name,
            "total": row.total
        })

    return jsonify({
        "message": "Sample analytics from BigQuery public dataset",
        "top_names": names
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)