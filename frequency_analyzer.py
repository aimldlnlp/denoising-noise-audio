import numpy as np
from scipy import signal
from typing import Tuple, Dict, List

class FrequencyAnalyzer:
    """
    A class to perform comprehensive frequency analysis on audio signals.
    Now includes FIR filtering for noise removal.
    """
    
    def __init__(self, signal: np.ndarray, sample_rate: int):
        """
        Initialize the FrequencyAnalyzer with a signal and its sample rate.
        """
        self.signal = signal
        self.sample_rate = sample_rate
    
    def compute_fft(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the Fast Fourier Transform (FFT) of the signal.
        Returns:
            - frequencies: Array of frequency bins
            - magnitudes: Corresponding magnitude values
        """
        fft_values = np.fft.fft(self.signal)
        frequencies = np.fft.fftfreq(len(self.signal), 1/self.sample_rate)
        magnitudes = np.abs(fft_values)
        
        # Return only positive frequencies
        positive_freq_mask = frequencies >= 0
        return frequencies[positive_freq_mask], magnitudes[positive_freq_mask]
    
    def compute_power_spectral_density(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the Power Spectral Density (PSD) using Welch’s method.
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
        """
        frequencies, magnitudes = self.compute_fft()
        
        # Sort frequencies by magnitude in descending order
        sorted_indices = np.argsort(magnitudes)[::-1]
        
        return {
            frequencies[idx]: magnitudes[idx] 
            for idx in sorted_indices[:top_n]
        }
    
    def compute_noise_characteristics(self) -> Dict[str, float]:
        """
        Compute noise characteristics of the signal.
        """
        rms = np.sqrt(np.mean(self.signal**2))
        
        _, psd = self.compute_power_spectral_density()
        noise_floor = np.mean(psd)
        
        signal_power = np.mean(self.signal**2)
        noise_power = noise_floor
        snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        
        return {
            'rms_amplitude': rms,
            'noise_floor': noise_floor,
            'signal_to_noise_ratio': snr
        }
    
    def design_fir_filter(self, stopbands: List[Tuple[int, int]], num_taps: int = 101) -> np.ndarray:
        """
        Design an FIR band-stop filter to remove noise frequencies.
        
        Args:
            stopbands (List[Tuple[int, int]]): List of (low, high) cutoff frequencies to remove
            num_taps (int): Number of filter coefficients
        
        Returns:
            np.ndarray: FIR filter coefficients
        """
        nyquist = self.sample_rate / 2
        
        # Convert stopbands into passbands
        bands = [0]  # Start from DC (0 Hz)
        desired = [1]  # Pass the DC component
        
        for low, high in sorted(stopbands):  # Ensure the frequencies are sorted
            bands.extend([low / nyquist, high / nyquist])
            desired.extend([0, 0])  # Attenuate this range

        bands.append(1)  # Extend to Nyquist frequency
        desired.append(1)  # Pass the rest of the signal
        
        # Ensure the frequency array is non-decreasing
        if not all(bands[i] <= bands[i + 1] for i in range(len(bands) - 1)):
            raise ValueError("Frequency values must be nondecreasing")
        
        fir_coeffs = signal.firwin2(num_taps, bands, desired, window="hamming")
        return fir_coeffs
    
    def apply_fir_filter(self, fir_coeffs: np.ndarray) -> np.ndarray:
        """
        Apply the designed FIR filter to the signal.
        
        Args:
            fir_coeffs (np.ndarray): FIR filter coefficients
        
        Returns:
            np.ndarray: Filtered signal
        """
        return signal.lfilter(fir_coeffs, 1.0, self.signal)
