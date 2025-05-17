import torch
from src.models.model import ConditionedUnet
def load_model(model_path, device):
    """
    Load the trained model
    """
    model = ConditionedUnet().to(device)
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model_epoch = checkpoint['epoch']
    model.eval()
    return model,model_epoch