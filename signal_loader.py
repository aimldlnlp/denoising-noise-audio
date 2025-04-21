import numpy as np
import soundfile as sf
from typing import Tuple

class SignalLoader:
    """
    A class to load and preprocess audio signals.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.signal = None
        self.sample_rate = None
    
    def load_signal(self) -> Tuple[np.ndarray, int]:
        """
        Load the audio signal from the file.
        """
        try:
            self.signal, self.sample_rate = sf.read(self.file_path)
            if self.signal.ndim > 1:
                self.signal = np.mean(self.signal, axis=1)
            return self.signal, self.sample_rate
        except FileNotFoundError:
            raise FileNotFoundError(f"Audio file not found: {self.file_path}")
        except Exception as e:
            raise ValueError(f"Error loading audio file: {str(e)}")
    
    def normalize_signal(self, signal: np.ndarray = None) -> np.ndarray:
        """
        Normalize the audio signal to the range [-1, 1].
        """
        if signal is None:
            signal = self.signal
        
        if signal is None:
            raise ValueError("No signal loaded. Call load_signal() first.")
        
        return signal / np.max(np.abs(signal))
    
    def save_signal(self, signal: np.ndarray, output_path: str):
        """
        Save the processed signal as an audio file.
        """
        sf.write(output_path, signal, self.sample_rate)
