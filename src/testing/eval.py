import os
import sys
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from torch.utils.data import DataLoader
from diffusers import DDPMScheduler
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.testing.dataset import mriDataset
from src.utils.logger import create_logger
from src.utils.load_config import load_config
from src.testing.load_model import load_model

__logger = create_logger(logger_name="eval_logger",
                         log_file="runtime/logs/eval.log", level=1)

def sample(model, scheduler, condition_image, timesteps, device):
    with torch.no_grad():
        noise = torch.randn_like(condition_image)
        residual = noise
        _mask = [[timesteps[len(timesteps)-i-1] for i in range(20)][::-1][-3]]
        for t in tqdm(_mask, desc="Sampling", leave=False):
            condition = scheduler.add_noise(condition_image, noise,torch.tensor([t]).to(device))
            residual = model(residual, torch.tensor([t]).to(device), condition)
        image = scheduler.step(residual,t,condition).pred_original_sample
        return image

def evaluate_model(config):
    # Setup device
    if config["device"] == "auto":
        device = 'mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = config["device"]
    __logger.info(f'Using device: {device}')
    
    # Load the dataset
    test_dataset = mriDataset(
        json_path=config["dataset"]["json_path"],
        resized=tuple(config["dataset"]["resized"])
    )
    
    test_dataloader = DataLoader(
        test_dataset, 
        batch_size=config["evaluation"]["batch_size"], 
        shuffle=False
    )
    
    # Load model
    model,_ = load_model(config["model"]["weights_path"], device)
    
    noise_scheduler = DDPMScheduler(
        num_train_timesteps=config["scheduler"]["num_train_timesteps"], 
        beta_schedule=config["scheduler"]["beta_schedule"]
    )

    # Create output directories
    os.makedirs(config["evaluation"]["output_dir"], exist_ok=True)
    os.makedirs(os.path.join(config["evaluation"]["output_dir"], "visualizations"), exist_ok=True)
    
    for idx, (img_id, mri3T) in enumerate(tqdm(test_dataloader, desc="Evaluating")):
        x = mri3T.to(device) * 2 - 1
        
        sampling_timesteps = list(range(0, config["scheduler"]["num_train_timesteps"], 
                                       config["evaluation"]["sampling_stride"]))[::-1]
        pred = sample(model, noise_scheduler, x, sampling_timesteps, device)
        
        pred_np = ((pred[0, 0].cpu().numpy() + 1) / 2).clip(0, 1)
        input_np = ((x[0, 0].cpu().numpy() + 1) / 2).clip(0, 1)
        import scipy.ndimage as ndimage

        # Resize the numpy arrays
        target_size = (364, 448)
        pred = torch.nn.functional.interpolate(pred, size=target_size, mode='bilinear', align_corners=False)
        pred_np = ndimage.zoom(pred_np, (target_size[0] / pred_np.shape[0], target_size[1] / pred_np.shape[1]), order=1)
        input_np = ndimage.zoom(input_np, (target_size[0] / input_np.shape[0], target_size[1] / input_np.shape[1]), order=1)
        
        # Create visualization
        if idx < config["evaluation"]["num_visualizations"]:
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(input_np, cmap='gray')
            axes[0].set_title(f"Input 3T MRI")
            axes[0].axis('off')
            
            axes[1].imshow(pred_np, cmap='gray')
            axes[1].set_title(f"Predicted resMap")
            axes[1].axis('off')
            
            axes[2].imshow(pred_np+input_np, cmap='gray')
            axes[2].set_title(f"Predicted 7T MRI")
            axes[2].axis('off')

            plt.tight_layout()
            plt.savefig(os.path.join(config["evaluation"]["output_dir"], 
                                     "visualizations", f"{img_id[0]}.png"))
            plt.close()


if __name__ == "__main__":
    # Load configuration
    config_path = "configs/test_config.yaml"
    config = load_config(config_path)
    
    __logger.info(f"Starting evaluation with config from: {config_path}")
    evaluate_model(config)