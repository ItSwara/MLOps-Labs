import numpy as np
import joblib
import os

# ── Load model & scaler ────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "svm_model.pkl")

artifact   = joblib.load(MODEL_PATH)
model      = artifact["model"]
scaler     = artifact["scaler"]

FEATURES = ["island", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex"]

# ── Encodings (must match LabelEncoder order from train.py) ───────────────────
ISLAND_MAP = {"Biscoe": 0, "Dream": 1, "Torgersen": 2}
SEX_MAP    = {"Female": 0, "Male": 1}

def predict_species(bill_length, bill_depth, flipper_length, body_mass, island, sex):
    # Encode categoricals
    island_enc = ISLAND_MAP.get(island, -1)
    sex_enc    = SEX_MAP.get(sex, -1)

    if island_enc == -1 or sex_enc == -1:
        raise ValueError(f"Invalid island '{island}' or sex '{sex}'")

    import pandas as pd
    input_data = pd.DataFrame([[
        island_enc, bill_length, bill_depth, flipper_length, body_mass, sex_enc
    ]], columns=FEATURES)

    # Scale
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction  = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0]
    confidence  = round(float(max(probability)) * 100, 1)

    return prediction, confidence


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    species, confidence = predict_species(
        bill_length=39.1,
        bill_depth=18.7,
        flipper_length=181.0,
        body_mass=3750,
        island="Torgersen",
        sex="Male"
    )
    print(f"Predicted Species : {species}")
    print(f"Confidence        : {confidence}%")