import numpy as np
import soundfile as sf
from typing import Tuple

class SignalLoader:
    """
    A class to load and preprocess audio signals for frequency analysis.
    
    Attributes:
        file_path (str): Path to the audio file
        signal (np.ndarray): Loaded audio signal
        sample_rate (int): Sampling rate of the audio
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the SignalLoader with the given audio file.
        
        Args:
            file_path (str): Path to the audio file
        """
        self.file_path = file_path
        self.signal = None
        self.sample_rate = None
    
    def load_signal(self) -> Tuple[np.ndarray, int]:
        """
        Load the audio signal from the file.
        
        Returns:
            Tuple containing the audio signal and its sample rate
        
        Raises:
            FileNotFoundError: If the audio file cannot be found
            ValueError: If there are issues reading the audio file
        """
        try:
            self.signal, self.sample_rate = sf.read(self.file_path)
            
            # Convert to mono if stereo
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
        
        Args:
            signal (np.ndarray, optional): Input signal to normalize. 
                                           Uses self.signal if not provided.
        
        Returns:
            np.ndarray: Normalized signal
        """
        if signal is None:
            signal = self.signal
        
        if signal is None:
            raise ValueError("No signal loaded. Call load_signal() first.")
        
        # Normalize to range [-1, 1]
        return signal / np.max(np.abs(signal))