import joblib

fcs_features = joblib.load("models/fcs_features.pkl")
rcsi_features = joblib.load("models/rcsi_features.pkl")
hhs_features = joblib.load("models/hhs_features.pkl")

print("\nFCS FEATURES")
print("=" * 50)
print(fcs_features)

print("\nrCSI FEATURES")
print("=" * 50)
print(rcsi_features)

print("\nHHS FEATURES")
print("=" * 50)
print(hhs_features)