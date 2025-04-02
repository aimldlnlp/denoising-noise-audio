import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal

class SignalVisualizer:
    """
    A class to visualize audio signals and their frequency components.
    """
    
    @staticmethod
    def plot_filter_response(fir_coeffs: np.ndarray, sample_rate: int, save_path: str = None):
        """
        Plot the frequency response of the FIR filter.
        """
        w, h = signal.freqz(fir_coeffs, worN=8000)
        plt.figure(figsize=(12, 4))
        plt.plot((w / np.pi) * (sample_rate / 2), abs(h))
        plt.title('FIR Filter Frequency Response')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.grid()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
