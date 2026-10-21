import torch, pickle

# 1. Load your PyTorch Deep Residual MLP weights
state_dict = torch.load("models/dataset_specialized/cic_ids2017/deep_model.pt", map_location="cpu")
print(f"Loaded PyTorch model with {len(state_dict)} weight tensors!")

# 2. Load your Tier-1 Classical screener
with open("models/dataset_specialized/cic_ids2017/classical_model.pkl", "rb") as f:
    classical_model = pickle.load(f)
print(f"Loaded Classical model: {type(classical_model).__name__}")