import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
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
    clustering_data = df[["Sleep_Duration", "Sleep_Quality", "Caffeine_Intake", "Screen_Time", "Physical_Activity"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    # bytes -> base64 string for XCom
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data_b64: str, filename: str):
    """
    Builds a KMeans model on the preprocessed data and saves it.
    Uses elbow method to find optimal k, then trains final model with that k.
    Returns the SSE list (JSON-serializable).
    """
    # decode -> bytes -> numpy array
    data_bytes = base64.b64decode(data_b64)
    df = pickle.loads(data_bytes)

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
    sse = []
    
    # Test different k values to find the elbow
    for k in range(1, 50):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

    # Find optimal k using elbow method
    kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")
    optimal_k = kl.elbow
    print(f"Building final model with optimal k={optimal_k}")

    # Train final model with optimal k
    final_kmeans = KMeans(n_clusters=optimal_k, **kmeans_kwargs)
    final_kmeans.fit(df)

    # Save the final optimized model
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        pickle.dump(final_kmeans, f)

    print(f"Model saved with {optimal_k} clusters")
    return sse  # list is JSON-safe


def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved model and uses the elbow method to report k.
    Returns the first prediction (as a plain int) for test.csv.
    """
    # load the saved (optimized) model
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(output_path, "rb"))

    # elbow for information/logging
    kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")
    print(f"Optimal no. of clusters for sleep patterns: {kl.elbow}")

    # predict on test data
    test_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    test_features = test_df[["Sleep_Duration", "Sleep_Quality", "Caffeine_Intake", "Screen_Time", "Physical_Activity"]]
    
    # Scale the test features
    scaler = MinMaxScaler()
    test_features_scaled = scaler.fit_transform(test_features)
    
    predictions = loaded_model.predict(test_features_scaled)
    
    print(f"Test students assigned to clusters: {list(predictions)}")

    # Return first prediction
    try:
        return int(predictions[0])
    except Exception:
        return predictions[0].item() if hasattr(predictions[0], "item") else predictions[0]