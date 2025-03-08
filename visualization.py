# noise_analysis/visualization.py
import matplotlib.pyplot as plt
import numpy as np
import os

class SignalVisualizer:
    """
    A class to visualize audio signals and their frequency components.
    Includes methods to save plots to a results directory.
    """
    
    @staticmethod
    def _ensure_results_dir(results_dir: str):
        """
        Ensure the results directory exists.
        
        Args:
            results_dir (str): Directory to store results
        
        Returns:
            str: Path to the results directory
        """
        os.makedirs(results_dir, exist_ok=True)
        return results_dir
    
    @staticmethod
    def plot_time_domain(signal: np.ndarray, sample_rate: int, 
                          title: str = 'Signal in Time Domain', 
                          save_path: str = None):
        """
        Plot the signal in the time domain.
        
        Args:
            signal (np.ndarray): Input audio signal
            sample_rate (int): Sampling rate of the signal
            title (str, optional): Plot title
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(12, 4))
        time = np.linspace(0, len(signal) / sample_rate, num=len(signal))
        plt.plot(time, signal)
        plt.title(title)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.tight_layout()
        
        if save_path:
            SignalVisualizer._ensure_results_dir(os.path.dirname(save_path))
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_frequency_spectrum(frequencies: np.ndarray, magnitudes: np.ndarray, 
                                 title: str = 'Frequency Spectrum', 
                                 save_path: str = None):
        """
        Plot the frequency spectrum.
        
        Args:
            frequencies (np.ndarray): Array of frequencies
            magnitudes (np.ndarray): Corresponding magnitude values
            title (str, optional): Plot title
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(12, 4))
        plt.plot(frequencies, magnitudes)
        plt.title(title)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.xscale('log')
        plt.grid(True)
        plt.tight_layout()
        
        if save_path:
            SignalVisualizer._ensure_results_dir(os.path.dirname(save_path))
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def plot_power_spectral_density(frequencies: np.ndarray, psd: np.ndarray, 
                                     title: str = 'Power Spectral Density', 
                                     save_path: str = None):
        """
        Plot the Power Spectral Density.
        
        Args:
            frequencies (np.ndarray): Array of frequencies
            psd (np.ndarray): Power Spectral Density values
            title (str, optional): Plot title
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(12, 4))
        plt.semilogy(frequencies, psd)
        plt.title(title)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.grid(True)
        plt.tight_layout()
        
        if save_path:
            SignalVisualizer._ensure_results_dir(os.path.dirname(save_path))
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
    
    @staticmethod
    def save_analysis_results(dominant_frequencies: dict, 
                               noise_characteristics: dict, 
                               results_dir: str):
        """
        Save analysis results to a text file.
        
        Args:
            dominant_frequencies (dict): Dictionary of dominant frequencies
            noise_characteristics (dict): Dictionary of noise characteristics
            results_dir (str): Directory to save results
        
        Returns:
            str: Path to the saved results file
        """
        # Ensure results directory exists
        SignalVisualizer._ensure_results_dir(results_dir)
        
        # Create results file path
        results_file = os.path.join(results_dir, 'noise_analysis_results.txt')
        
        # Write results to file
        with open(results_file, 'w') as f:
            f.write("Dominant Frequencies:\n")
            for freq, mag in dominant_frequencies.items():
                f.write(f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}\n")
            
            f.write("\nNoise Characteristics:\n")
            for name, value in noise_characteristics.items():
                f.write(f"{name}: {value}\n")
        
        return results_file