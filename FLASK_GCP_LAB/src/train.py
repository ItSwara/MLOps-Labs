import os
import joblib
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_PATH  = os.path.join(os.path.dirname(__file__), "data", "penguins.csv")
MODEL_DIR  = os.path.join(os.path.dirname(__file__), "..", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "svm_model.pkl")

# ── Load ───────────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} rows")
    return df

# ── Preprocess ─────────────────────────────────────────────────────────────────
def preprocess(df):
    # Drop noise columns
    df = df.drop(columns=["id", "year"], errors="ignore")

    # Drop rows with missing values
    df = df.dropna()
    print(f"After dropping nulls: {len(df)} rows")

    # Encode categoricals
    df["island"] = LabelEncoder().fit_transform(df["island"])
    df["sex"]    = LabelEncoder().fit_transform(df["sex"])

    X = df.drop(columns=["species"])
    y = df["species"]

    return X, y

# ── Train ──────────────────────────────────────────────────────────────────────
def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    model = SVC(kernel="rbf", C=1.0, gamma="scale", probability=True)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, scaler

# ── Save ───────────────────────────────────────────────────────────────────────
def save_model(model, scaler):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({"model": model, "scaler": scaler}, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df            = load_data()
    X, y          = preprocess(df)
    model, scaler = train(X, y)
    save_model(model, scaler)