import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

# 1. Load data
# Can switch between sharp_trade.csv, static_trade.csv, or label_trade.csv
file_path = './sharp_trade.csv'
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# 2. Identify Features and Target
exclude_cols = ['Date', 'Label', 'Signal']
feature_cols = [c for c in df.columns if c not in exclude_cols]
print(f"Using features: {feature_cols}")

prediction_days = 10
target_map = {-1: 0, 0: 1, 1: 2}
df['SignalClass'] = df['Signal'].map(target_map).astype(int)

# 3. Split data
train_end = int(len(df) * 0.8)
train_df = df.iloc[:train_end].copy().reset_index(drop=True)
test_df = df.iloc[train_end - prediction_days:].copy().reset_index(drop=True)

# 4. Scale features
scaler = StandardScaler()
train_feats = scaler.fit_transform(train_df[feature_cols].values)
test_feats = scaler.transform(test_df[feature_cols].values)

def build_sequences(features_arr: np.ndarray, class_series: pd.Series, timesteps: int):
    X, y = [], []
    for i in range(timesteps, len(features_arr)):
        X.append(features_arr[i - timesteps:i])
        y.append(class_series.iloc[i])
    return np.array(X), np.array(y)


X_train, y_train = build_sequences(train_feats, train_df['SignalClass'], prediction_days)
X_test, y_test = build_sequences(test_feats, test_df['SignalClass'], prediction_days)

print("Shapes:", X_train.shape, y_train.shape, X_test.shape, y_test.shape)

# 5. Convert to categorical (one-hot) for multi-class classification
n_classes = 3 # Fixed to 3: Sell(-1), Neutral(0), Buy(1)
y_train_cat = to_categorical(y_train, num_classes=n_classes)
y_test_cat = to_categorical(y_test, num_classes=n_classes)

# 6. Build LSTM model
n_features = X_train.shape[2]
model = Sequential()
model.add(LSTM(64, input_shape=(prediction_days, n_features), return_sequences=False))
model.add(Dropout(0.3))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(n_classes, activation='softmax'))  # multi-class

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# 7. Train
history = model.fit(
    X_train, y_train_cat,
    validation_data=(X_test, y_test_cat),
    epochs=20,
    batch_size=32,
    verbose=2
)

# 8. Evaluate
pred_probs = model.predict(X_test)
pred_classes = np.argmax(pred_probs, axis=1)

acc = accuracy_score(y_test, pred_classes)
print(f"\nTest accuracy: {acc:.4f}\n")
print("Classification report (test):")
print(classification_report(y_test, pred_classes, target_names=['Sell(-1)', 'NoSignal(0)', 'Buy(1)']))

print("Confusion matrix:")
print(confusion_matrix(y_test, pred_classes))

# 9. Save model
# model.save('lstm_signal_model.h5')
