import numpy as np
from skimage.metrics import structural_similarity, peak_signal_noise_ratio

def calculate_psnr(img1, img2):
    """
    Calculate PSNR (Peak Signal-to-Noise Ratio) between two images
    Higher values indicate better quality
    """
    return peak_signal_noise_ratio(img1, img2, data_range=1.0)

def calculate_ssim(img1, img2):
    """
    Calculate SSIM (Structural Similarity Index) between two images
    Higher values indicate better structural similarity (max 1.0)
    """
    return structural_similarity(img1, img2, data_range=1.0)