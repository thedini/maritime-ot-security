---
title: "Lab 11"
subtitle: "Machine Learning Anomaly Detection"
author: "Constantine Macris"
date: "2026"
titlepage: true
titlepage-color: "1E3A5F"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
description: |
    Implementing ML-based intrusion detection for CAN bus
---

# Lab 11 -- Machine Learning Anomaly Detection

## Lab Overview

**Duration**: 2 hours
**Prerequisites**: Labs 09-10 completed, Class 11 material reviewed
**Materials Required**:
- Python 3.x with scikit-learn, numpy
- Normal and attack captures
- (Optional) PyTorch for LSTM

## Objectives

By the end of this lab, you will:

1. Extract features from CAN messages
2. Train One-Class SVM on normal traffic
3. Train Random Forest classifier (if labeled data available)
4. Evaluate model performance
5. Compare ML to statistical methods

## Part 1: Feature Engineering (30 minutes)

### 1.1 Design Feature Set

```python
#!/usr/bin/env python3
"""
ml_detection.py - ML-based CAN anomaly detection
"""
import numpy as np
from collections import defaultdict, Counter
import math

class FeatureExtractor:
    def __init__(self, window_size=100):
        """
        Extract features from CAN message windows

        Args:
            window_size: Number of messages per feature window
        """
        self.window_size = window_size
        self.feature_names = self._define_features()

    def _define_features(self):
        """Define feature names for documentation"""
        return [
            'unique_can_ids',
            'unique_pgns',
            'unique_sas',
            'can_id_entropy',
            'pgn_entropy',
            'sa_entropy',
            'data_entropy',
            'mean_interval',
            'std_interval',
            'min_interval',
            'max_interval',
            'pgn_127250_count',  # Heading
            'pgn_129025_count',  # Position
            'pgn_129026_count',  # COG/SOG
            'pgn_130306_count',  # Wind
            'data_mean',
            'data_std',
            'data_zeros_ratio',
            'data_ff_ratio',
        ]

    def extract(self, messages):
        """
        Extract features from message window

        Args:
            messages: List of dicts with 'can_id', 'data', 'timestamp'

        Returns:
            numpy array of features
        """
        if len(messages) < self.window_size:
            return None

        # Take last window_size messages
        window = messages[-self.window_size:]

        # Extract base data
        can_ids = [m['can_id'] for m in window]
        pgns = [(m['can_id'] >> 8) & 0x3FFFF for m in window]
        sas = [m['can_id'] & 0xFF for m in window]
        timestamps = [m['timestamp'] for m in window]
        all_bytes = []
        for m in window:
            all_bytes.extend(m['data'])

        # Calculate features
        features = []

        # Uniqueness
        features.append(len(set(can_ids)))
        features.append(len(set(pgns)))
        features.append(len(set(sas)))

        # Entropy
        features.append(self._entropy(can_ids))
        features.append(self._entropy(pgns))
        features.append(self._entropy(sas))
        features.append(self._entropy(all_bytes))

        # Timing
        intervals = [timestamps[i] - timestamps[i-1]
                     for i in range(1, len(timestamps))]
        if intervals:
            features.append(np.mean(intervals))
            features.append(np.std(intervals))
            features.append(np.min(intervals))
            features.append(np.max(intervals))
        else:
            features.extend([0, 0, 0, 0])

        # PGN counts
        pgn_counts = Counter(pgns)
        features.append(pgn_counts.get(127250, 0))
        features.append(pgn_counts.get(129025, 0))
        features.append(pgn_counts.get(129026, 0))
        features.append(pgn_counts.get(130306, 0))

        # Data byte statistics
        features.append(np.mean(all_bytes))
        features.append(np.std(all_bytes))
        features.append(sum(1 for b in all_bytes if b == 0) / len(all_bytes))
        features.append(sum(1 for b in all_bytes if b == 0xFF) / len(all_bytes))

        return np.array(features)

    def _entropy(self, values):
        """Calculate Shannon entropy"""
        counter = Counter(values)
        total = len(values)
        entropy = 0
        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def extract_batch(self, all_messages, step=50):
        """
        Extract features from entire message stream

        Args:
            all_messages: List of all messages
            step: Step size between windows

        Returns:
            Feature matrix (n_samples, n_features)
        """
        features_list = []
        timestamps = []

        for i in range(self.window_size, len(all_messages), step):
            window = all_messages[i-self.window_size:i]
            features = self.extract(window)
            if features is not None:
                features_list.append(features)
                timestamps.append(window[-1]['timestamp'])

        return np.array(features_list), timestamps
```

### 1.2 Extract Features from Captures

```python
def load_messages(capture_file):
    """Load messages from capture file"""
    messages = []
    with open(capture_file) as f:
        for line in f:
            msg = parse_message(line)  # Use your parser
            if msg:
                messages.append(msg)
    return messages

# Load normal traffic
normal_messages = load_messages('normal_capture.txt')
print(f"Loaded {len(normal_messages)} normal messages")

# Extract features
extractor = FeatureExtractor(window_size=100)
X_normal, ts_normal = extractor.extract_batch(normal_messages, step=50)
print(f"Extracted {X_normal.shape[0]} feature vectors")
print(f"Feature dimension: {X_normal.shape[1]}")
```

### 1.3 Verify Feature Statistics

```python
# Print feature statistics
print("\nFeature Statistics (Normal Traffic):")
print("=" * 60)
for i, name in enumerate(extractor.feature_names):
    values = X_normal[:, i]
    print(f"{name:25s}: mean={np.mean(values):.3f}, "
          f"std={np.std(values):.3f}, "
          f"range=[{np.min(values):.3f}, {np.max(values):.3f}]")
```

## Part 2: One-Class SVM (30 minutes)

### 2.1 Implement SVM Detector

```python
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib

class SVMDetector:
    def __init__(self, kernel='rbf', nu=0.05):
        """
        One-Class SVM anomaly detector

        Args:
            kernel: SVM kernel type
            nu: Upper bound on fraction of outliers
        """
        self.model = OneClassSVM(kernel=kernel, nu=nu, gamma='auto')
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, X_normal):
        """
        Train on normal traffic

        Args:
            X_normal: Feature matrix of normal traffic
        """
        print(f"Training SVM on {X_normal.shape[0]} samples...")

        # Scale features
        X_scaled = self.scaler.fit_transform(X_normal)

        # Train
        self.model.fit(X_scaled)
        self.is_trained = True

        # Evaluate on training data
        scores = self.model.decision_function(X_scaled)
        predictions = self.model.predict(X_scaled)
        inlier_rate = np.mean(predictions == 1)

        print(f"Training complete")
        print(f"  Inlier rate on training: {inlier_rate:.2%}")
        print(f"  Decision scores: mean={np.mean(scores):.3f}, "
              f"std={np.std(scores):.3f}")

        return inlier_rate

    def predict(self, X):
        """
        Predict anomaly

        Args:
            X: Feature vector or matrix

        Returns:
            predictions: 1=normal, -1=anomaly
            scores: Decision function values (lower = more anomalous)
        """
        if not self.is_trained:
            raise ValueError("Model not trained")

        X = np.atleast_2d(X)
        X_scaled = self.scaler.transform(X)

        predictions = self.model.predict(X_scaled)
        scores = self.model.decision_function(X_scaled)

        return predictions, scores

    def save(self, filepath):
        """Save model to file"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, filepath)

    def load(self, filepath):
        """Load model from file"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = True
```

### 2.2 Train SVM

```python
# Create and train detector
svm_detector = SVMDetector(kernel='rbf', nu=0.05)
svm_detector.train(X_normal)
svm_detector.save('svm_model.joblib')
```

### 2.3 Test on Normal Data

```python
# Test on held-out normal data
from sklearn.model_selection import train_test_split

X_train, X_test = train_test_split(X_normal, test_size=0.3, random_state=42)

# Retrain on training portion
svm_detector = SVMDetector(kernel='rbf', nu=0.05)
svm_detector.train(X_train)

# Test
predictions, scores = svm_detector.predict(X_test)
normal_test_rate = np.mean(predictions == 1)
print(f"Normal test set: {normal_test_rate:.2%} classified as normal")
```

**Record:**
- Normal test accuracy: _______ %
- False positive rate: _______ %

### 2.4 Test on Attack Data

```python
# Load attack traffic
attack_messages = load_messages('dos_attack_capture.txt')
X_attack, _ = extractor.extract_batch(attack_messages, step=50)

# Predict
predictions, scores = svm_detector.predict(X_attack)
attack_detect_rate = np.mean(predictions == -1)
print(f"Attack detection rate: {attack_detect_rate:.2%}")
```

**Record detection rates:**

| Attack | Samples | Detected | Rate |
|--------|---------|----------|------|
| DoS | | | |
| Spoofing | | | |
| Replay | | | |

## Part 3: Random Forest (if labeled data) (20 minutes)

### 3.1 Prepare Labeled Dataset

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Combine normal and attack data with labels
X_combined = np.vstack([X_normal, X_attack])
y_combined = np.array([0] * len(X_normal) + [1] * len(X_attack))

# Shuffle and split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, y_combined, test_size=0.3, random_state=42, stratify=y_combined
)

print(f"Training: {len(X_train)} samples")
print(f"  Normal: {np.sum(y_train == 0)}")
print(f"  Attack: {np.sum(y_train == 1)}")
```

### 3.2 Train Random Forest

```python
class RandomForestDetector:
    def __init__(self, n_estimators=100, max_depth=10):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = None

    def train(self, X_train, y_train, feature_names=None):
        """Train classifier"""
        self.feature_names = feature_names
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)

        # Get feature importance
        importances = self.model.feature_importances_
        if feature_names:
            importance_pairs = sorted(zip(feature_names, importances),
                                     key=lambda x: x[1], reverse=True)
            print("\nTop 5 Features:")
            for name, imp in importance_pairs[:5]:
                print(f"  {name}: {imp:.4f}")

    def predict(self, X):
        """Predict class and probability"""
        X_scaled = self.scaler.transform(np.atleast_2d(X))
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        return predictions, probabilities

# Train
rf_detector = RandomForestDetector(n_estimators=100, max_depth=10)
rf_detector.train(X_train, y_train, extractor.feature_names)

# Evaluate
predictions, probs = rf_detector.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, predictions,
                           target_names=['Normal', 'Attack']))
```

### 3.3 Record Results

**Random Forest Results:**
- Accuracy: _______ %
- Precision (Attack): _______ %
- Recall (Attack): _______ %
- F1 Score: _______

**Top 5 Features:**
1. _________________ : _______
2. _________________ : _______
3. _________________ : _______
4. _________________ : _______
5. _________________ : _______

## Part 4: Model Comparison (15 minutes)

### 4.1 Compare All Methods

```python
def evaluate_all_methods(X_test_normal, X_test_attack):
    """Compare all detection methods"""
    results = {}

    # Frequency-based (from Lab 09)
    # ... load and test

    # Entropy-based (from Lab 10)
    # ... load and test

    # SVM
    svm = SVMDetector()
    svm.load('svm_model.joblib')
    svm_pred_n, _ = svm.predict(X_test_normal)
    svm_pred_a, _ = svm.predict(X_test_attack)
    results['SVM'] = {
        'fpr': np.mean(svm_pred_n == -1),
        'tpr': np.mean(svm_pred_a == -1)
    }

    # Random Forest (if available)
    # ...

    return results
```

### 4.2 Comparison Table

| Method | False Positive Rate | True Positive Rate | F1 |
|--------|--------------------|--------------------|-----|
| Frequency | | | |
| Entropy | | | |
| One-Class SVM | | | |
| Random Forest | | | |

### 4.3 Analysis

Answer in your report:
1. Which method has best overall performance?
2. Which method has lowest false positive rate?
3. Which attacks are each method best/worst at detecting?
4. What are the computational requirements of each?

## Part 5: Real-Time Considerations (10 minutes)

### 5.1 Measure Inference Time

```python
import time

def benchmark_prediction(model, X_sample, n_iterations=1000):
    """Benchmark prediction latency"""
    times = []

    for _ in range(n_iterations):
        start = time.perf_counter()
        model.predict(X_sample)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        'mean_ms': np.mean(times) * 1000,
        'std_ms': np.std(times) * 1000,
        'max_ms': np.max(times) * 1000,
        'throughput': 1.0 / np.mean(times)
    }

# Benchmark SVM
svm_bench = benchmark_prediction(svm_detector, X_test[0:1])
print(f"SVM: {svm_bench['mean_ms']:.3f}ms/prediction "
      f"({svm_bench['throughput']:.0f}/sec)")
```

### 5.2 Latency Results

| Method | Mean (ms) | Max (ms) | Throughput |
|--------|-----------|----------|------------|
| SVM | | | |
| Random Forest | | | |

**Target: < 1ms for real-time at 10Hz message rate**

## Deliverables

Submit via course portal:

1. **ml_detection.py** - Feature extractor and models
2. **svm_model.joblib** - Trained SVM
3. **Comparison table** - All methods compared
4. **Lab report** - Including analysis

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| Feature extraction correct | 20 |
| SVM trained and tested | 25 |
| Random Forest (or comparison) | 20 |
| Method comparison complete | 20 |
| Performance analysis | 15 |
| **Total** | **100** |

## Next Lab Preview

In Lab 12, you will:
- Implement device fingerprinting
- Calculate clock skew
- Build fingerprint database
- Test impersonation detection
