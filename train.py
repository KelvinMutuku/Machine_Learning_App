from pathlib import Path
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_DIR = Path("predictor") / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "iris_rf.joblib"

def main():
    data = load_iris()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    joblib.dump(
        {
            "estimator": clf,
            "target_names": data.target_names,
            "feature_names": data.feature_names,
        },
        MODEL_PATH,
    )
    print(f"Saved model to {MODEL_PATH.resolve()}")

if __name__ == "__main__":
    main()