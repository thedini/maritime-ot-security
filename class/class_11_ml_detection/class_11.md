---
title: "Class 11"
subtitle: "Machine Learning for Anomaly Detection"
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
    Applying SVM, Random Forest, and LSTM to CAN bus intrusion detection
---

# Class 11 -- Machine Learning for Anomaly Detection

## Learning Outcomes

- Understand supervised vs unsupervised anomaly detection
- Implement SVM-based CAN message classification
- Apply Random Forest to attack detection
- Build LSTM autoencoder for sequence anomalies
- Evaluate and compare ML model performance

## Definitions

- **Supervised Learning** -- Training with labeled examples
- **Unsupervised Learning** -- Finding patterns without labels
- **Feature Engineering** -- Creating ML-ready inputs from raw data
- **Autoencoder** -- Neural network that learns to compress and reconstruct
- **Reconstruction Error** -- Difference between input and reconstructed output
- **Anomaly Score** -- Measure of how unusual a sample is

## Reading Assignment

- Literature Review: Section 4.2 (ML-Based Detection)
- Literature Review: Section 6.4 (Jeep Cherokee detection methods)
- scikit-learn documentation on anomaly detection

## Why Machine Learning?

### Limitations of Statistical Methods

| Method | Limitation |
|--------|------------|
| Frequency | Only catches rate anomalies |
| Entropy | Only catches distribution shifts |
| Rules | Only catches known patterns |

### ML Advantages

1. **Learn complex patterns**: Non-linear relationships
2. **Adapt to data**: No manual threshold tuning
3. **Generalize**: Detect novel attacks
4. **Combine features**: Multi-dimensional analysis

### ML Challenges

1. **Labeled data**: Need examples of attacks
2. **Overfitting**: May not generalize
3. **Computational cost**: Real-time constraints
4. **Interpretability**: "Black box" decisions

<!--
Instructor Notes:

ML is powerful but not magic!

Key points:
1. Need good training data (garbage in = garbage out)
2. Feature engineering is critical
3. Model selection depends on data/constraints
4. Always validate on unseen data

For CAN bus:
- Labeled attacks are scarce (simulate)
- Real-time constraints (model size matters)
- Interpretability important for security
-->

## Feature Engineering for CAN

### Raw Data to Features

CAN message: `(timestamp, can_id, data[8])`

Transform to features:

```python
import numpy as np
from collections import defaultdict

class CANFeatureExtractor:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.message_buffer = []
        self.timestamp_buffer = []

    def add_message(self, timestamp, can_id, data):
        """Add message to buffer"""
        self.message_buffer.append((can_id, data))
        self.timestamp_buffer.append(timestamp)

        # Maintain window
        while len(self.message_buffer) > self.window_size:
            self.message_buffer.pop(0)
            self.timestamp_buffer.pop(0)

    def extract_features(self):
        """Extract features from current window"""
        if len(self.message_buffer) < self.window_size:
            return None

        features = {}

        # ID-based features
        can_ids = [msg[0] for msg in self.message_buffer]
        unique_ids = set(can_ids)

        features['unique_ids'] = len(unique_ids)
        features['id_entropy'] = self._entropy(can_ids)

        # Frequency features (per common PGN)
        pgn_counts = defaultdict(int)
        for can_id, _ in self.message_buffer:
            pgn = (can_id >> 8) & 0x3FFFF
            pgn_counts[pgn] += 1

        for pgn in [127250, 129025, 129026, 130306]:
            features[f'pgn_{pgn}_count'] = pgn_counts.get(pgn, 0)

        # Timing features
        intervals = []
        for i in range(1, len(self.timestamp_buffer)):
            intervals.append(self.timestamp_buffer[i] - self.timestamp_buffer[i-1])

        if intervals:
            features['mean_interval'] = np.mean(intervals)
            features['std_interval'] = np.std(intervals)
            features['min_interval'] = np.min(intervals)
            features['max_interval'] = np.max(intervals)

        # Data byte features
        all_bytes = []
        for _, data in self.message_buffer:
            all_bytes.extend(data)

        features['data_entropy'] = self._entropy(all_bytes)
        features['data_mean'] = np.mean(all_bytes)
        features['data_std'] = np.std(all_bytes)

        return features

    def _entropy(self, values):
        from collections import Counter
        import math

        counter = Counter(values)
        total = len(values)
        entropy = 0.0

        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def to_vector(self, features):
        """Convert feature dict to vector for ML"""
        feature_names = sorted(features.keys())
        return np.array([features[name] for name in feature_names])
```

### Feature Selection

| Feature | Detects | Importance |
|---------|---------|------------|
| unique_ids | New devices | High |
| id_entropy | DoS | High |
| pgn_X_count | Rate changes | Medium |
| mean_interval | Overall rate | Medium |
| std_interval | Timing jitter | Medium |
| data_entropy | Content changes | High |

<!--
Instructor Notes:

Feature engineering is 80% of the work!

Good features:
- Capture attack signatures
- Are normalized/comparable
- Are computationally cheap
- Have clear meaning

Bad features:
- Raw timestamps (not normalized)
- Arbitrary byte positions (not meaningful)
- High-dimensional (slow to process)

Lab exercise: Experiment with different features.
-->

## Support Vector Machine (SVM)

### SVM for Anomaly Detection

One-Class SVM learns "normal" boundary:
- Train on normal traffic only
- Points outside boundary = anomalies

```python
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import numpy as np

class SVMAnomalyDetector:
    def __init__(self, kernel='rbf', nu=0.1):
        """
        One-Class SVM anomaly detector

        Args:
            kernel: SVM kernel ('rbf', 'linear', 'poly')
            nu: Upper bound on fraction of anomalies (0.1 = 10%)
        """
        self.model = OneClassSVM(kernel=kernel, nu=nu)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, normal_features):
        """
        Train on normal traffic features

        Args:
            normal_features: Array of feature vectors (n_samples, n_features)
        """
        # Scale features
        X = self.scaler.fit_transform(normal_features)

        # Train one-class SVM
        self.model.fit(X)
        self.is_trained = True

        # Calculate training accuracy
        predictions = self.model.predict(X)
        normal_rate = np.sum(predictions == 1) / len(predictions)

        return {'normal_rate': normal_rate}

    def predict(self, features):
        """
        Predict if sample is anomaly

        Args:
            features: Single feature vector or array

        Returns:
            is_anomaly: True if anomaly, False if normal
            score: Decision function value (lower = more anomalous)
        """
        if not self.is_trained:
            raise ValueError("Model not trained")

        # Reshape if single sample
        if len(features.shape) == 1:
            features = features.reshape(1, -1)

        # Scale
        X = self.scaler.transform(features)

        # Predict
        predictions = self.model.predict(X)
        scores = self.model.decision_function(X)

        # Convert: -1 = anomaly, 1 = normal
        is_anomaly = predictions[0] == -1
        score = scores[0]

        return is_anomaly, score
```

### Using SVM Detector

```python
# Build training data (normal traffic)
extractor = CANFeatureExtractor(window_size=100)
training_features = []

for timestamp, can_id, data in normal_traffic:
    extractor.add_message(timestamp, can_id, data)
    features = extractor.extract_features()
    if features:
        training_features.append(extractor.to_vector(features))

X_train = np.array(training_features)

# Train detector
detector = SVMAnomalyDetector(nu=0.05)  # Expect 5% outliers
result = detector.train(X_train)
print(f"Training normal rate: {result['normal_rate']:.2%}")

# Detect attacks
for timestamp, can_id, data in test_traffic:
    extractor.add_message(timestamp, can_id, data)
    features = extractor.extract_features()
    if features:
        is_anomaly, score = detector.predict(extractor.to_vector(features))
        if is_anomaly:
            print(f"ALERT: Anomaly detected at {timestamp}, score={score:.3f}")
```

<!--
Instructor Notes:

SVM advantages:
- Works with small training sets
- Handles high-dimensional data well
- Clear decision boundary

SVM disadvantages:
- Sensitive to kernel/parameter choice
- Not probabilistic (no confidence score)
- Doesn't capture temporal patterns

For CAN: Good baseline method, especially with
limited labeled data. Use nu to control sensitivity.
-->

## Random Forest Classifier

### Supervised Attack Classification

With labeled data, use supervised learning:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class RandomForestDetector:
    def __init__(self, n_estimators=100, max_depth=10):
        """
        Random Forest attack classifier

        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = None

    def train(self, features, labels, feature_names=None):
        """
        Train classifier

        Args:
            features: Array of feature vectors
            labels: Array of labels (0=normal, 1=attack, or attack type)
            feature_names: List of feature names for importance
        """
        self.feature_names = feature_names

        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            features, labels, test_size=0.2, random_state=42
        )

        # Scale
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)

        # Train
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_val_scaled)
        report = classification_report(y_val, y_pred, output_dict=True)

        return report

    def predict(self, features):
        """Predict attack type"""
        X = self.scaler.transform(features.reshape(1, -1))
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]

        return prediction, probabilities

    def get_feature_importance(self):
        """Get feature importance rankings"""
        importances = self.model.feature_importances_
        if self.feature_names:
            return sorted(zip(self.feature_names, importances),
                         key=lambda x: x[1], reverse=True)
        return importances
```

### Attack Type Classification

```python
# Labels: 0=normal, 1=dos, 2=spoof, 3=replay
labels_map = {
    'normal': 0,
    'dos': 1,
    'spoofing': 2,
    'replay': 3
}

# Train multi-class classifier
detector = RandomForestDetector(n_estimators=200)
report = detector.train(X_train, y_train, feature_names=feature_names)

print("Classification Report:")
print(f"Accuracy: {report['accuracy']:.2%}")
print(f"DoS F1: {report['1']['f1-score']:.2%}")
print(f"Spoofing F1: {report['2']['f1-score']:.2%}")
print(f"Replay F1: {report['3']['f1-score']:.2%}")

# Feature importance
print("\nTop Features:")
for name, importance in detector.get_feature_importance()[:5]:
    print(f"  {name}: {importance:.3f}")
```

<!--
Instructor Notes:

Random Forest advantages:
- Handles mixed feature types
- Provides feature importance
- Robust to overfitting
- Easy to interpret

Random Forest disadvantages:
- Needs labeled data (supervised)
- May be large (many trees)
- Doesn't capture sequence patterns

Feature importance is valuable:
- Shows what matters for detection
- Guides feature engineering
- Explains model decisions
-->

## LSTM Autoencoder

### Sequence-Based Detection

LSTM captures temporal patterns:
- Normal sequences reconstructed well
- Attack sequences have high reconstruction error

```python
import torch
import torch.nn as nn

class LSTMAutoencoder(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, latent_dim=16, num_layers=2):
        """
        LSTM Autoencoder for sequence anomaly detection

        Args:
            input_dim: Number of features per timestep
            hidden_dim: LSTM hidden dimension
            latent_dim: Encoded representation size
            num_layers: Number of LSTM layers
        """
        super().__init__()

        # Encoder
        self.encoder_lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        self.encoder_fc = nn.Linear(hidden_dim, latent_dim)

        # Decoder
        self.decoder_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder_lstm = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        self.output_fc = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        """Encode sequence to latent representation"""
        # x shape: (batch, seq_len, input_dim)
        lstm_out, (h_n, c_n) = self.encoder_lstm(x)
        # Use last hidden state
        latent = self.encoder_fc(h_n[-1])
        return latent

    def decode(self, z, seq_len):
        """Decode latent representation to sequence"""
        # Repeat latent for each timestep
        hidden = self.decoder_fc(z)
        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)

        # Decode through LSTM
        lstm_out, _ = self.decoder_lstm(hidden)
        output = self.output_fc(lstm_out)
        return output

    def forward(self, x):
        """Full forward pass"""
        seq_len = x.shape[1]
        latent = self.encode(x)
        reconstruction = self.decode(latent, seq_len)
        return reconstruction
```

### Training LSTM Autoencoder

```python
class LSTMDetector:
    def __init__(self, input_dim, seq_len=10, device='cpu'):
        self.device = device
        self.seq_len = seq_len
        self.model = LSTMAutoencoder(input_dim).to(device)
        self.scaler = StandardScaler()
        self.threshold = None

    def create_sequences(self, features):
        """Create sequences for LSTM"""
        sequences = []
        for i in range(len(features) - self.seq_len + 1):
            seq = features[i:i + self.seq_len]
            sequences.append(seq)
        return np.array(sequences)

    def train(self, normal_features, epochs=50, batch_size=32):
        """Train autoencoder on normal traffic"""
        # Scale features
        features_scaled = self.scaler.fit_transform(normal_features)

        # Create sequences
        sequences = self.create_sequences(features_scaled)
        X = torch.FloatTensor(sequences).to(self.device)

        # Training setup
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3)
        criterion = nn.MSELoss()

        # Training loop
        self.model.train()
        losses = []

        for epoch in range(epochs):
            total_loss = 0
            n_batches = len(X) // batch_size

            for i in range(0, len(X), batch_size):
                batch = X[i:i+batch_size]

                optimizer.zero_grad()
                reconstruction = self.model(batch)
                loss = criterion(reconstruction, batch)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            avg_loss = total_loss / n_batches
            losses.append(avg_loss)

            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.6f}")

        # Set threshold based on training reconstruction errors
        self.model.eval()
        with torch.no_grad():
            reconstruction = self.model(X)
            errors = torch.mean((X - reconstruction) ** 2, dim=(1, 2))
            self.threshold = torch.mean(errors) + 3 * torch.std(errors)

        return losses

    def predict(self, features):
        """Detect anomaly based on reconstruction error"""
        # Scale
        features_scaled = self.scaler.transform(features.reshape(1, -1))

        # Need full sequence - this is simplified
        # In practice, maintain a buffer of recent features

        self.model.eval()
        with torch.no_grad():
            X = torch.FloatTensor(features_scaled).unsqueeze(0).to(self.device)
            reconstruction = self.model(X)
            error = torch.mean((X - reconstruction) ** 2).item()

        is_anomaly = error > self.threshold.item()
        return is_anomaly, error
```

<!--
Instructor Notes:

LSTM Autoencoder advantages:
- Captures temporal patterns
- Unsupervised (no labels needed)
- Learns complex sequences
- Adaptable to different traffic

LSTM disadvantages:
- Requires more data to train
- Computationally expensive
- Harder to interpret
- Needs careful tuning

For CAN bus:
- Works well for sequence attacks (replay)
- May miss single-message anomalies
- Consider hybrid approaches

Lab: Train on OpenPlotter baseline, test on attacks.
-->

## Model Comparison

### Evaluation Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

def evaluate_detector(y_true, y_pred, y_scores=None):
    """
    Comprehensive detector evaluation

    Args:
        y_true: True labels (0=normal, 1=attack)
        y_pred: Predicted labels
        y_scores: Anomaly scores (for ROC AUC)

    Returns:
        Dictionary of metrics
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)
    }

    if y_scores is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_scores)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    metrics['true_negative'] = cm[0, 0]
    metrics['false_positive'] = cm[0, 1]
    metrics['false_negative'] = cm[1, 0]
    metrics['true_positive'] = cm[1, 1]

    return metrics
```

### Comparison Table

| Metric | SVM | Random Forest | LSTM |
|--------|-----|---------------|------|
| Training Data | Normal only | Labeled | Normal only |
| Temporal | No | No | Yes |
| Interpretable | Partial | Yes | No |
| Real-time | Yes | Yes | Depends |
| DoS Detection | Good | Excellent | Good |
| Spoofing | Good | Good | Good |
| Replay | Poor | Fair | Excellent |

## Practical Considerations

### Real-Time Constraints

```python
import time

def benchmark_detector(detector, test_data, n_iterations=1000):
    """Benchmark detector latency"""
    times = []

    for _ in range(n_iterations):
        sample = test_data[np.random.randint(len(test_data))]

        start = time.perf_counter()
        detector.predict(sample)
        elapsed = time.perf_counter() - start

        times.append(elapsed)

    return {
        'mean_ms': np.mean(times) * 1000,
        'std_ms': np.std(times) * 1000,
        'max_ms': np.max(times) * 1000,
        'throughput': 1.0 / np.mean(times)  # predictions/sec
    }

# Target: < 1ms per prediction for 10 Hz messages
```

### Model Deployment

```python
import joblib

def save_detector(detector, filepath):
    """Save trained detector"""
    state = {
        'model': detector.model,
        'scaler': detector.scaler,
        'threshold': detector.threshold,
        'config': detector.config
    }
    joblib.dump(state, filepath)

def load_detector(filepath, detector_class):
    """Load trained detector"""
    state = joblib.load(filepath)
    detector = detector_class.__new__(detector_class)
    detector.model = state['model']
    detector.scaler = state['scaler']
    detector.threshold = state['threshold']
    detector.config = state['config']
    return detector
```

## Lab Preview: Week 11

In Lab 11, you will:

1. Implement feature extraction for CAN messages
2. Train One-Class SVM on normal traffic
3. Train Random Forest with labeled attacks
4. Build and train LSTM autoencoder
5. Compare detection performance
6. Benchmark real-time latency

**Evaluation**: Accuracy, recall, F1, latency

## Homework

### Required

1. **Read**: Literature Review Section 4.2 completely
2. **Implement**: CANFeatureExtractor with at least 10 features
3. **Compare**: Pros/cons of supervised vs unsupervised for maritime

### Suggested

- Research: Isolation Forest for anomaly detection
- Explore: PyTorch LSTM tutorial
- Consider: How would you update models as traffic patterns change?

## Discussion Questions

1. Why is unsupervised learning often preferred for IDS?
2. How do you handle concept drift (changing normal behavior)?
3. What features best capture maritime attack signatures?
4. Should ML models be interpretable for security applications?

## References

- [scikit-learn Anomaly Detection]
- [PyTorch LSTM Tutorial]
- [ML-Based CAN IDS Research]

[scikit-learn Anomaly Detection]:https://scikit-learn.org/stable/modules/outlier_detection.html
[PyTorch LSTM Tutorial]:https://pytorch.org/tutorials/
[ML-Based CAN IDS Research]:https://ieeexplore.ieee.org
