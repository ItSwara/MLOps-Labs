from flask import Flask, request, jsonify
from predict import predict_species
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    bill_length    = float(data['bill_length_mm'])
    bill_depth     = float(data['bill_depth_mm'])
    flipper_length = float(data['flipper_length_mm'])
    body_mass      = float(data['body_mass_g'])
    island         = str(data['island'])
    sex            = str(data['sex'])

    print(bill_length, bill_depth, flipper_length, body_mass, island, sex)

    species, confidence = predict_species(
        bill_length, bill_depth, flipper_length, body_mass, island, sex
    )

    return jsonify({
        'prediction': species,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )