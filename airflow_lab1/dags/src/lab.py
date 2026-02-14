import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import os
import base64

def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("Loading sleep patterns data...")
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    serialized_data = pickle.dumps(df)                    # bytes
    return base64.b64encode(serialized_data).decode("ascii")  # JSON-safe string

def data_preprocessing(data_b64: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data.
    """
    # decode -> bytes -> DataFrame
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    # Select sleep-related features for clustering
    clustering_data = df[["Sleep_Duration", "Caffeine_Intake", "Screen_Time", "Physical_Activity"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    # bytes -> base64 string for XCom
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a RandomForestRegressor model on the preprocessed data and saves it.
    Returns a list (JSON-safe) similar to SSE list (we return per-tree OOB-like proxy is not available without oob).
    We'll return a simple list with one value: train RMSE (still JSON-safe list).
    """
    # decode -> bytes -> numpy array (scaled features) AND y (we'll rebuild y from file.csv to keep flow same)
    data_bytes = base64.b64decode(data_b64)
    X_scaled = pickle.loads(data_bytes)

    # Load the original df again to get y (keeping overall structure unchanged)
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    df = df.dropna()

    # Target
    y = df["Sleep_Quality"].values

    # Train Random Forest
    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_scaled, y)

    # Save BOTH model + scaler used in preprocessing
    # (We reload and refit the scaler exactly like your preprocessing did, to keep consistency)
    clustering_data = df[["Sleep_Duration", "Caffeine_Intake", "Screen_Time", "Physical_Activity"]]
    scaler = MinMaxScaler()
    scaler.fit(clustering_data)

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "wb") as f:
        pickle.dump({"model": rf, "scaler": scaler}, f)

    # Return a list to keep DAG/XCom contract same as your SSE list
    preds_train = rf.predict(X_scaled)
    rmse_train = mean_squared_error(y, preds_train, squared=False)

    print(f"RandomForestRegressor saved. Train RMSE: {rmse_train:.4f}")
    return [float(rmse_train)]



def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved RandomForestRegressor model and predicts Sleep_Quality for test.csv.
    Keeps the same function name/signature as your original file.
    Returns the first prediction (float).
    """
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    saved = pickle.load(open(output_path, "rb"))
    loaded_model = saved["model"]
    scaler = saved["scaler"]

    # This list is no longer SSE/elbow, but we keep it for compatibility
    if sse and len(sse) == 1:
        print(f"(RF) Train RMSE (from build_save_model): {sse[0]}")
    else:
        print("(RF) No SSE/elbow in Random Forest; ignoring elbow logic.")

    # predict on test data
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    test_features = test_df[["Sleep_Duration", "Caffeine_Intake", "Screen_Time", "Physical_Activity"]]

    # Scale test features using the SAME scaler saved from training
    test_features_scaled = scaler.transform(test_features)

    predictions = loaded_model.predict(test_features_scaled)

    print(f"Predicted Sleep_Quality for test students: {list(map(float, predictions))}")

    # Return first prediction (keep behavior similar)
    try:
        return float(predictions[0])
    except Exception:
        return predictions[0].item() if hasattr(predictions[0], "item") else predictions[0]
