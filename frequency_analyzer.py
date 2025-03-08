import numpy as np
from scipy import signal
from typing import Tuple, Dict

class FrequencyAnalyzer:
    """
    A class to perform comprehensive frequency analysis on audio signals.
    
    Attributes:
        signal (np.ndarray): Input audio signal
        sample_rate (int): Sampling rate of the signal
    """
    
    def __init__(self, signal: np.ndarray, sample_rate: int):
        """
        Initialize the FrequencyAnalyzer with a signal and its sample rate.
        
        Args:
            signal (np.ndarray): Input audio signal
            sample_rate (int): Sampling rate of the signal
        """
        self.signal = signal
        self.sample_rate = sample_rate
    
    def compute_fft(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the Fast Fourier Transform of the signal.
        
        Returns:
            Tuple of frequencies and their magnitudes
        """
        # Compute FFT
        fft_values = np.fft.fft(self.signal)
        frequencies = np.fft.fftfreq(len(self.signal), 1/self.sample_rate)
        
        # Compute magnitude spectrum
        magnitudes = np.abs(fft_values)
        
        # Return only positive frequencies
        positive_freq_mask = frequencies >= 0
        return frequencies[positive_freq_mask], magnitudes[positive_freq_mask]
    
    def compute_power_spectral_density(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the Power Spectral Density using Welch's method.
        
        Returns:
            Tuple of frequencies and power spectral density
        """
        frequencies, psd = signal.welch(
            self.signal, 
            fs=self.sample_rate, 
            nperseg=1024
        )
        return frequencies, psd
    
    def identify_dominant_frequencies(self, top_n: int = 5) -> Dict[float, float]:
        """
        Identify the top N dominant frequencies in the signal.
        
        Args:
            top_n (int, optional): Number of top frequencies to return. Defaults to 5.
        
        Returns:
            Dict of dominant frequencies and their magnitudes
        """
        frequencies, magnitudes = self.compute_fft()
        
        # Sort frequencies by magnitude in descending order
        sorted_indices = np.argsort(magnitudes)[::-1]
        
        # Return top N dominant frequencies
        dominant_freq_dict = {
            frequencies[idx]: magnitudes[idx] 
            for idx in sorted_indices[:top_n]
        }
        
        return dominant_freq_dict
    
    def compute_noise_characteristics(self) -> Dict[str, float]:
        """
        Compute noise characteristics of the signal.
        
        Returns:
            Dict of noise characteristics
        """
        # Compute signal RMS
        rms = np.sqrt(np.mean(self.signal**2))
        
        # Compute noise floor using PSD
        _, psd = self.compute_power_spectral_density()
        noise_floor = np.mean(psd)
        
        # Compute signal-to-noise ratio (approximate)
        signal_power = np.mean(self.signal**2)
        noise_power = noise_floor
        snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        
        return {
            'rms_amplitude': rms,
            'noise_floor': noise_floor,
            'signal_to_noise_ratio': snr
        }