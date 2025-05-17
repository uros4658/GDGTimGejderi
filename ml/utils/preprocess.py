import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def load_and_preprocess(path, window_size=10):
    df = pd.read_csv(path)
    df['eta'] = pd.to_datetime(df['eta'])
    df = df.sort_values('eta')

    # Features to use
    num_cols = ['loa_m', 'beam_m', 'draft_m']
    cat_cols = ['vessel_type']

    # Scale numeric
    num_scaler = StandardScaler()
    X_num = num_scaler.fit_transform(df[num_cols])

    # Encode categorical
    enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_cat = enc.fit_transform(df[cat_cols])

    # Join features
    X_full = np.hstack([X_num, X_cat])
    X_seq, y = [], []

    for i in range(len(X_full) - window_size):
        window = X_full[i:i+window_size]
        label = df.iloc[i+window_size]['optimizer_berth_id']
        X_seq.append(window)
        y.append(label)

    return np.array(X_seq), np.array(y), num_scaler, enc
