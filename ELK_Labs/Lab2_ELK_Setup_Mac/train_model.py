import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix, classification_report
import numpy as np

# Configure the logging module
logging.basicConfig(filename='lab6_training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Breast Cancer Wisconsin dataset
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = data.feature_names
target_names = data.target_names

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Logging important information
logging.info("=" * 60)
logging.info("ELK Lab - Swarali Degaonkar")
logging.info("=" * 60)
logging.info("Starting model training...")
logging.info(f"Dataset: Breast Cancer Wisconsin")
logging.info(f"Algorithm: Random Forest Classifier")
logging.info(f"Hyperparameters: n_estimators=100, max_depth=10, random_state=42")
logging.info(f"Number of features: {X.shape[1]}")
logging.info(f"Number of training samples: {len(X_train)}")
logging.info(f"Number of testing samples: {len(X_test)}")
logging.info(f"Class distribution (train): Malignant={sum(y_train == 0)}, Benign={sum(y_train == 1)}")
logging.info(f"Class distribution (test): Malignant={sum(y_test == 0)}, Benign={sum(y_test == 1)}")

# Training the model and logging progress
model.fit(X_train, y_train)
logging.info("Model training completed.")

# Evaluate the model
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
logging.info(f"Model accuracy on test data: {score:.4f}")

# Additional metrics
f1 = f1_score(y_test, predictions, average='weighted')
conf_matrix = confusion_matrix(y_test, predictions)

tn, fp, fn, tp = conf_matrix.ravel()

# Log metrics
logging.info(f"F1 Score (weighted): {f1:.4f}")
logging.info(f"True Negative: {tn}")
logging.info(f"False Positive: {fp}")
logging.info(f"False Negative: {fn}")
logging.info(f"True Positive: {tp}")
logging.info(f"False Positive Rate: {fp / (fp + tn):.4f}")
logging.info(f"False Negative Rate: {fn / (fn + tp):.4f}")
logging.info(f"Precision (Malignant): {tn / (tn + fn):.4f}")
logging.info(f"Recall (Malignant): {tn / (tn + fp):.4f}")
logging.info(f"Precision (Benign): {tp / (tp + fp):.4f}")
logging.info(f"Recall (Benign): {tp / (tp + fn):.4f}")

# Log top 10 feature importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
logging.info("Top 10 Feature Importances:")
for i in range(10):
    logging.info(f"  {feature_names[indices[i]]}: {importances[indices[i]]:.4f}")

logging.info("Training pipeline completed successfully.")







# import logging
# from sklearn.linear_model import LogisticRegression
# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import f1_score, confusion_matrix
# import numpy as np

# # Configure the logging module
# logging.basicConfig(filename='training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Load the Iris dataset
# data = load_iris()
# X, y = data.data, data.target

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize the Logistic Regression model
# model = LogisticRegression()

# # Logging important information
# logging.info("Starting model training...")
# logging.info(f"Number of training samples: {len(X_train)}")
# logging.info(f"Number of testing samples: {len(X_test)}")

# # Training the model and logging progress
# model.fit(X_train, y_train)
# logging.info("Model training completed.")

# # Evaluate the model
# predictions = model.predict(X_test)
# score = model.score(X_test, y_test)
# logging.info(f"Model accuracy on test data: {score:.2f}")

# # Additional metrics
# f1 = f1_score(y_test, predictions, average='weighted')  # Use 'weighted' for multiclass F1 score
# conf_matrix = confusion_matrix(y_test, predictions)

# tp = np.diag(conf_matrix)
# tn = np.sum(conf_matrix) - (np.sum(conf_matrix, axis=0) + np.sum(conf_matrix, axis=1) - tp)
# fp = np.sum(conf_matrix, axis=0) - tp
# fn = np.sum(conf_matrix, axis=1) - tp
# # Log additional metric
# fp_rate = fp / (fp + tn)
# fn_rate = fn / (fn + tp)

# # Log additional metrics
# logging.info(f"F1 Score: {f1:.2f}")
# logging.info(f"True Negative: {tn}")
# logging.info(f"False Positive: {fp}")
# logging.info(f"False Negative: {fn}")
# logging.info(f"True Positive: {tp}")
# logging.info(f"False Positive Rate: {fp_rate:}")
# logging.info(f"False Negative Rate: {fn_rate:}")

# # Log model parameters
# logging.info(f"Model coefficients: {model.coef_}")
# logging.info(f"Model intercept: {model.intercept_}")
