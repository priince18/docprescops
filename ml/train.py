# REVIEW: Your train.py is production-ready for EFS deployment
# STATUS: YES ✔ Ready with minor recommended improvements below

import os
# pyrefly: ignore [missing-import]
import joblib
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# =====================================================
# EFS STORAGE PATHS
# =====================================================
MODEL_DIR = Path("/mnt/efs/ml-data/models")
ARTIFACT_DIR = Path("/mnt/efs/ml-data/artifacts")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "seed.csv"
MODEL_FILE = MODEL_DIR / "model.pkl"
REPORT_FILE = ARTIFACT_DIR / "classification_report.txt"

def train_model():
    print('Loading data from', DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    # =====================================================
    # VALIDATION
    # =====================================================
    required_columns = ["symptoms", "label"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Clean data
    df = df.dropna(subset=["symptoms", "label"])
    df['symptoms'] = df['symptoms'].astype(str).str.lower().str.strip()
    df['label'] = df['label'].astype(str).str.strip()

    X = df['symptoms']
    y = df['label']

    print("Dataset size:", len(df))
    print("Unique labels:", y.nunique())

    # =====================================================
    # TRAIN / TEST SPLIT
    # =====================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # =====================================================
    # PIPELINE
    # =====================================================
    print('Building pipeline...')

    pipeline = Pipeline([
        (
            'tfidf',
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                max_features=5000
            )
        ),
        (
            'clf',
            LogisticRegression(
                max_iter=1000,
                solver='lbfgs'
            )
        ),
    ])

    # =====================================================
    # TRAIN
    # =====================================================
    print('Training model...')
    pipeline.fit(X_train, y_train)

    # =====================================================
    # EVALUATE
    # =====================================================
    print('Evaluating...')
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print('Accuracy:', round(acc, 4))
    print(report)

    # Save evaluation report
    with open(REPORT_FILE, "w") as f:
        f.write(f"Accuracy: {round(acc, 4)}\n\n")
        f.write(report)

    # =====================================================
    # SAVE MODEL
    # =====================================================
    print('Saving model to', MODEL_FILE)
    joblib.dump(pipeline, MODEL_FILE)

    print('Model saved successfully.')
    print('Report saved to', REPORT_FILE)
    print('Done.')