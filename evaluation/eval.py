import numpy as np
from scipy.io import wavfile
from scipy.signal import welch  # Corrected import

def compute_snr(noisy_signal, clean_signal):
    """
    Compute the Signal-to-Noise Ratio (SNR) between noisy and clean signals.
    
    Parameters:
        noisy_signal (numpy array): The noisy signal.
        clean_signal (numpy array): The filtered (clean) signal.
    
    Returns:
        float: The SNR value in dB.
    """
    # Ensure both signals are of the same length
    min_len = min(len(noisy_signal), len(clean_signal))
    noisy_signal = noisy_signal[:min_len]
    clean_signal = clean_signal[:min_len]
    
    noise = noisy_signal - clean_signal
    signal_power = np.sum(clean_signal ** 2)
    noise_power = np.sum(noise ** 2)

    if noise_power == 0:
        return np.inf  # No noise at all
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def spectral_flatness(signal, fs, nperseg=1024):
    """
    Compute Spectral Flatness of a signal using the Welch method.
    
    Parameters:
        signal (numpy array): The signal to compute spectral flatness for.
        fs (int): The sampling rate of the signal.
        nperseg (int): Length of each segment for analysis (default: 1024).
    
    Returns:
        tuple: Spectral flatness value, frequency, and Power Spectral Density (PSD).
    """
    f, Pxx = welch(signal, fs=fs, nperseg=nperseg)  # Corrected to use scipy.signal.welch
    Pxx = np.maximum(Pxx, 1e-12)  # Prevent log(0)
    geometric_mean = np.exp(np.mean(np.log(Pxx)))
    arithmetic_mean = np.mean(Pxx)
    flatness = geometric_mean / arithmetic_mean
    return flatness, f, Pxx

def load_wav(file_path):
    """
    Load a WAV file and return the sampling rate and signal.
    
    Parameters:
        file_path (str): Path to the WAV file.
    
    Returns:
        tuple: Sampling rate and signal from the WAV file.
    """
    fs, signal = wavfile.read(file_path)
    return fs, signal

def main(noisy_file, filtered_file):
    """
    Main function to process both WAV files, calculate SNR and Spectral Flatness,
    and display the results.
    
    Parameters:
        noisy_file (str): Path to the noisy WAV file.
        filtered_file (str): Path to the filtered (cleaned) WAV file.
    """
    # Load WAV files
    fs_noisy, noisy_signal = load_wav(noisy_file)
    fs_filtered, filtered_signal = load_wav(filtered_file)

    # Ensure both signals have the same sampling rate
    if fs_noisy != fs_filtered:
        raise ValueError("The sampling rates of both files must be the same!")

    # Calculate SNR
    snr = compute_snr(noisy_signal, filtered_signal)
    print(f"SNR (Filtered vs Noisy): {snr:.2f} dB")

    # Calculate Spectral Flatness
    flat_noisy, _, _ = spectral_flatness(noisy_signal, fs_noisy)
    flat_filtered, _, _ = spectral_flatness(filtered_signal, fs_filtered)

    print(f"Spectral Flatness - Noisy: {flat_noisy:.4f}")
    print(f"Spectral Flatness - Filtered: {flat_filtered:.4f}")

if __name__ == "__main__":
    noisy_file = "dataset/seg_1.wav"
    filtered_file = "results/seg_1/filtered_audio.wav"
    
    main(noisy_file, filtered_file)