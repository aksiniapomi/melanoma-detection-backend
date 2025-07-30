from sklearn.model_selection import train_test_split
import numpy as np

# load all features & labels from the .npz
d = np.load("data/cnn_features.npz")
X = np.vstack([d["X_train"], d["X_val"], d["X_test"]])
y = np.concatenate([d["y_train"], d["y_val"], d["y_test"]])

# stratified 80/20 split
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("New Train:", X_tr.shape[0])
print("New Test: ", X_te.shape[0])
print("Total:    ", X_tr.shape[0] + X_te.shape[0])
