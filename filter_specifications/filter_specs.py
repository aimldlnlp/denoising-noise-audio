import numpy as np
import soundfile as sf
from scipy.fft import fft, fftfreq
from typing import List, Tuple
import os

def load_audio(file_path: str) -> Tuple[np.ndarray, int]:
    """
    Load the audio signal from a WAV file.
    
    Args:
        file_path (str): Path to the WAV file.
        
    Returns:
        Tuple[np.ndarray, int]: Audio signal as a numpy array and the sample rate.
    """
    signal, sample_rate = sf.read(file_path)
    if signal.ndim > 1:  # If stereo, convert to mono
        signal = np.mean(signal, axis=1)
    return signal, sample_rate

def calculate_fft(signal: np.ndarray, sample_rate: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform FFT on the audio signal to obtain frequency and magnitude data.
    
    Args:
        signal (np.ndarray): The audio signal to analyze.
        sample_rate (int): The sample rate of the audio.
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Frequencies and magnitudes of the FFT.
    """
    N = len(signal)
    frequencies = fftfreq(N, d=1/sample_rate)[:N//2]  # Only positive frequencies
    magnitudes = np.abs(fft(signal))[:N//2]  # Magnitudes of the FFT
    return frequencies, magnitudes

def calculate_passband_ripple(frequencies: np.ndarray, magnitudes: np.ndarray, passband: Tuple[float, float]) -> float:
    """
    Calculate the Passband Ripple (dB) as the difference between the max and min magnitude within the passband.
    
    Args:
        frequencies (np.ndarray): Frequency values.
        magnitudes (np.ndarray): Corresponding magnitudes of the frequency response.
        passband (Tuple[float, float]): The frequency range representing the passband (low, high).
    
    Returns:
        float: Passband Ripple in dB.
    """
    passband_indices = np.where((frequencies >= passband[0]) & (frequencies <= passband[1]))[0]
    passband_magnitudes = magnitudes[passband_indices]
    
    passband_ripple = 20 * np.log10(np.max(passband_magnitudes) / np.min(passband_magnitudes))
    return passband_ripple

def calculate_relative_side_lobe_level(frequencies: np.ndarray, magnitudes: np.ndarray, main_frequency: float) -> float:
    """
    Calculate the Relative Side Lobe Level (dB), the ratio of the side lobe magnitude to the main lobe magnitude.
    
    Args:
        frequencies (np.ndarray): Frequency values.
        magnitudes (np.ndarray): Corresponding magnitudes of the frequency response.
        main_frequency (float): The frequency of the main peak.
    
    Returns:
        float: Relative Side Lobe Level in dB.
    """
    main_peak_idx = np.argmin(np.abs(frequencies - main_frequency))
    main_peak_magnitude = magnitudes[main_peak_idx]
    
    side_lobe_magnitudes = np.concatenate([
        magnitudes[main_peak_idx-5:main_peak_idx],  # before the main peak
        magnitudes[main_peak_idx+1:main_peak_idx+6]  # after the main peak
    ])
    
    side_lobe_max = np.max(side_lobe_magnitudes)
    relative_side_lobe_level = 20 * np.log10(side_lobe_max / main_peak_magnitude)
    return relative_side_lobe_level

def calculate_stopband_attenuation(frequencies: np.ndarray, magnitudes: np.ndarray, stopband: Tuple[float, float]) -> float:
    """
    Calculate the maximum stopband attenuation (dB) in the stopband region.
    
    Args:
        frequencies (np.ndarray): Frequency values.
        magnitudes (np.ndarray): Corresponding magnitudes of the frequency response.
        stopband (Tuple[float, float]): The frequency range representing the stopband (low, high).
    
    Returns:
        float: Maximum stopband attenuation in dB.
    """
    stopband_indices = np.where((frequencies >= stopband[0]) & (frequencies <= stopband[1]))[0]
    stopband_magnitudes = magnitudes[stopband_indices]
    
    max_stopband_magnitude = np.max(stopband_magnitudes)
    stopband_attenuation = 20 * np.log10(max_stopband_magnitude)
    return stopband_attenuation

def get_passband_and_stopband(dominant_frequencies: list) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Define passband and stopband based on the dominant frequencies found in the audio signal.
    
    Args:
        dominant_frequencies (list): List of tuples where each tuple contains a frequency and its corresponding magnitude.
    
    Returns:
        Tuple: passband (low, high) and stopband (low, high).
    """
    sorted_frequencies = sorted(dominant_frequencies, key=lambda x: x[1], reverse=True)
    
    main_frequency = sorted_frequencies[0][0]
    
    passband = (main_frequency - 5, main_frequency + 5)
    
    stopband = (400, 450)
    
    return passband, stopband

def analyze_audio(audio_file_path: str):
    """
    Analyze the audio file and compute the filter specifications based on dominant frequencies.
    
    Args:
        audio_file_path (str): Path to the audio file.
    """
    # Load audio file and perform frequency analysis (replace this with your actual analysis logic)
    signal, sample_rate = load_audio(audio_file_path)  # Assuming this function exists
    
    # For demonstration, suppose you already have the top 5 dominant frequencies (from your analysis)
    dominant_frequencies = [
        ( 49.60 ,1275.58),
        ( 49.80, 987.81),
        ( 100.00, 78.35),
        ( 85.40 ,598.72),
        ( 86.40 ,583.94)
    ]
    
    passband, stopband = get_passband_and_stopband(dominant_frequencies)
    
    frequencies, magnitudes = calculate_fft(signal, sample_rate)
    
    passband_ripple = calculate_passband_ripple(frequencies, magnitudes, passband)
    side_lobe_level = calculate_relative_side_lobe_level(frequencies, magnitudes, dominant_frequencies[0][0])
    stopband_attenuation = calculate_stopband_attenuation(frequencies, magnitudes, stopband)
    
    print(f"Analysis results for {audio_file_path}:")
    print(f"Passband Ripple: {passband_ripple:.2f} dB")
    print(f"Relative Side Lobe Level: {side_lobe_level:.2f} dB")
    print(f"Stopband Maximum Attenuation: {stopband_attenuation:.2f} dB")

def main():
    # dataset_folder = "dataset"  # Path to the dataset folder
    
    # # Iterate through each audio file in the dataset
    # for audio_file in os.listdir(dataset_folder):
    #     if audio_file.endswith(".wav"):
    #         audio_file_path = os.path.join(dataset_folder, audio_file)
    #         analyze_audio(audio_file_path)

    audio_file_path = "dataset\seg_102.wav"
    analyze_audio(audio_file_path)

if __name__ == "_main_":
    main()