import torch
import joblib
import numpy as np
import json
import pandas as pd
from models.berth_lstm import BerthPlannerLSTM
from utils.preprocess import load_and_preprocess

# Load all data
X, y, _, _ = load_and_preprocess("data/vessel_calls.csv")

# Load model and encoders
model = BerthPlannerLSTM(input_size=X.shape[2], hidden_size=64, num_layers=1, output_size=4)
model.load_state_dict(torch.load("artifacts/berth_lstm.pt"))
model.eval()

le = joblib.load("artifacts/label_encoder.pkl")

# Predict for all vessels
berth_plan = []
with torch.no_grad():
    X_tensor = torch.tensor(X, dtype=torch.float32)
    out = model(X_tensor)
    pred_indices = torch.argmax(out, dim=1).numpy()
    pred_labels = le.inverse_transform(pred_indices)

    # Load vessel info from CSV for output
    df = pd.read_csv("data/vessel_calls.csv")
    for i in range(len(pred_labels)):
        row = df.iloc[i]
        berth_plan.append({
            "vessel": row.get("vessel_name", f"Vessel-{i+1}"),
            "eta": row["eta"],
            "berth": pred_labels[i]
        })

# Output as JSON
with open("berth_plan.json", "w") as f:
    json.dump(berth_plan, f, indent=2)

print(json.dumps(berth_plan, indent=2))