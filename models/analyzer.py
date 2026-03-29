import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyAnalyzer:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.15,
            random_state=42
        )
        self._train_on_synthetic_data()

    def _train_on_synthetic_data(self):
        # synthetic "normal" surface data for baseline training
        # features: [defect_ratio, mean_intensity, std_intensity, avg_perimeter, defect_count]
        np.random.seed(42)
        normal_data = np.column_stack([
            np.random.uniform(0.0, 0.02, 300),      # low defect ratio
            np.random.uniform(100, 200, 300),         # normal brightness
            np.random.uniform(10, 40, 300),           # low std dev
            np.random.uniform(0, 50, 300),            # small perimeters
            np.random.randint(0, 4, 300)              # few defects
        ])
        self.model.fit(normal_data)

    def predict(self, features: list) -> bool:
        sample = np.array(features).reshape(1, -1)
        prediction = self.model.predict(sample)
        return bool(prediction[0] == -1)  # -1 = anomaly in IsolationForest
