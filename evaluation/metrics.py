import numpy as np
from scipy.signal import welch
from typing import List, Tuple

def compute_snr(signal: np.ndarray, noise: np.ndarray) -> float:
    """Compute Signal-to-Noise Ratio (SNR) in dB."""
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    return 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')

def compute_spectral_flatness(signal: np.ndarray, sample_rate: int) -> float:
    """Compute Spectral Flatness Measure (SFM) — lower is cleaner/less noisy."""
    _, psd = welch(signal, fs=sample_rate, nperseg=1024)
    geometric_mean = np.exp(np.mean(np.log(psd + 1e-12)))  # Avoid log(0)
    arithmetic_mean = np.mean(psd)
    return geometric_mean / arithmetic_mean if arithmetic_mean > 0 else 0

def compute_band_energy(signal: np.ndarray, sample_rate: int, band: Tuple[float, float]) -> float:
    """Compute energy in a specific frequency band using Welch's method."""
    freqs, psd = welch(signal, fs=sample_rate, nperseg=1024)
    band_mask = (freqs >= band[0]) & (freqs <= band[1])
    return np.sum(psd[band_mask])