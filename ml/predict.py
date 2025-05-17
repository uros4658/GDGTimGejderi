import torch
import joblib
import numpy as np
from models.berth_lstm import BerthPlannerLSTM
from utils.preprocess import load_and_preprocess

# Load latest window
X, y, _, _ = load_and_preprocess("data/vessel_calls.csv")
X_input = torch.tensor(X[-1:], dtype=torch.float32)

# Load model and encoders
model = BerthPlannerLSTM(input_size=X.shape[2], hidden_size=64, num_layers=1, output_size=4)
model.load_state_dict(torch.load("artifacts/berth_lstm.pt"))
model.eval()

le = joblib.load("artifacts/label_encoder.pkl")

# Predict
with torch.no_grad():
    out = model(X_input)
    pred_idx = torch.argmax(out, dim=1).item()
    pred_label = le.inverse_transform([pred_idx])[0]
    print("🔮 Predicted berth:", pred_label)
