import cv2
import numpy as np
from models.analyzer import AnomalyAnalyzer


class DefectDetector:
    def __init__(self):
        self.analyzer = AnomalyAnalyzer()
        self.blur_kernel = (5, 5)
        self.canny_low = 50
        self.canny_high = 150
        self.min_contour_area = 100

    def preprocess(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        return gray, blurred

    def detect_edges(self, blurred):
        edges = cv2.Canny(blurred, self.canny_low, self.canny_high)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        return dilated

    def find_contours(self, edge_image):
        contours, _ = cv2.findContours(
            edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        filtered = [c for c in contours if cv2.contourArea(c) > self.min_contour_area]
        return filtered

    def extract_features(self, gray, contours):
        total_area = sum(cv2.contourArea(c) for c in contours)
        image_area = gray.shape[0] * gray.shape[1]
        defect_ratio = total_area / image_area if image_area > 0 else 0

        mean_intensity = float(np.mean(gray))
        std_intensity = float(np.std(gray))

        perimeters = [cv2.arcLength(c, True) for c in contours]
        avg_perimeter = float(np.mean(perimeters)) if perimeters else 0.0

        return [defect_ratio, mean_intensity, std_intensity, avg_perimeter, len(contours)]

    def classify_severity(self, defect_count, defect_ratio):
        if defect_count == 0:
            return "None", 0.0
        elif defect_count <= 3 and defect_ratio < 0.02:
            return "Low", round(0.4 + defect_ratio * 5, 2)
        elif defect_count <= 8 and defect_ratio < 0.08:
            return "Medium", round(0.6 + defect_ratio * 3, 2)
        else:
            return "High", round(min(0.95, 0.75 + defect_ratio), 2)

    def analyze(self, image_path: str) -> dict:
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Could not read image"}

        gray, blurred = self.preprocess(image)
        edges = self.detect_edges(blurred)
        contours = self.find_contours(edges)

        features = self.extract_features(gray, contours)
        defect_ratio = features[0]
        defect_count = len(contours)

        severity, confidence = self.classify_severity(defect_count, defect_ratio)
        is_anomaly = self.analyzer.predict(features)

        defect_regions = []
        for c in contours[:10]:
            x, y, w, h = cv2.boundingRect(c)
            area = round(float(cv2.contourArea(c)), 2)
            defect_regions.append({"x": x, "y": y, "w": w, "h": h, "area": area})

        return {
            "defect_count": defect_count,
            "severity": severity,
            "confidence": confidence,
            "is_anomaly": is_anomaly,
            "defect_ratio": round(defect_ratio * 100, 3),
            "mean_intensity": round(features[1], 2),
            "std_intensity": round(features[2], 2),
            "defect_regions": defect_regions,
            "image_size": {
                "width": image.shape[1],
                "height": image.shape[0]
            }
        }
