import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import os
from models.berth_lstm import BerthPlannerLSTM
from utils.preprocess import load_and_preprocess
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Parameters
window_size = 10
X, y, scaler, encoder = load_and_preprocess("data/vessel_calls.csv", window_size=window_size)

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)

# Model
model = BerthPlannerLSTM(
    input_size=X.shape[2],
    hidden_size=64,
    num_layers=1,
    output_size=len(le.classes_)
)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = loss_fn(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

# Save model & transformers
os.makedirs("artifacts", exist_ok=True)
torch.save(model.state_dict(), "artifacts/berth_lstm.pt")
joblib.dump(le, "artifacts/label_encoder.pkl")
joblib.dump(scaler, "artifacts/scaler.pkl")
joblib.dump(encoder, "artifacts/ohe.pkl")
print("✅ Model and encoders saved.")
