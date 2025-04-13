import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from typing import Tuple


class EnhancedSignalVisualizer:
    """A collection of static methods for visualizing and comparing original and filtered audio signals."""

    @staticmethod
    def plot_time_domain(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str) -> None:
        """Plot and save time-domain waveform comparison."""
        times = np.arange(len(before)) / sample_rate
        plt.figure(figsize=(14, 4))
        plt.plot(times, before, label='Original', alpha=0.6, linewidth=1)
        plt.plot(times, after, label='Filtered', alpha=0.8, linewidth=1)
        plt.title('Time Domain Signal Comparison')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_frequency_spectrum(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str) -> None:
        """Plot and save frequency-domain comparison using FFT."""
        def compute_fft(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)
            magnitude = np.abs(np.fft.rfft(data))
            return freqs, magnitude

        freqs_before, fft_before = compute_fft(before)
        freqs_after, fft_after = compute_fft(after)

        plt.figure(figsize=(14, 4))
        plt.plot(freqs_before, fft_before, label='Original', alpha=0.6, linewidth=1)
        plt.plot(freqs_after, fft_after, label='Filtered', alpha=0.8, linewidth=1)
        plt.title('Frequency Spectrum (FFT)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_psd(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str) -> None:
        """Plot and save Power Spectral Density using Welch’s method."""
        freqs_before, psd_before = signal.welch(before, fs=sample_rate, nperseg=1024)
        freqs_after, psd_after = signal.welch(after, fs=sample_rate, nperseg=1024)

        plt.figure(figsize=(14, 4))
        plt.semilogy(freqs_before, psd_before, label='Original', alpha=0.6, linewidth=1)
        plt.semilogy(freqs_after, psd_after, label='Filtered', alpha=0.8, linewidth=1)
        plt.title('Power Spectral Density (Welch Method)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_filter_kernel(fir_coeffs: np.ndarray, save_path: str) -> None:
        """Plot and save FIR filter impulse response."""
        plt.figure(figsize=(10, 3))
        plt.stem(fir_coeffs, use_line_collection=True, basefmt=" ", linefmt='b-', markerfmt='bo')
        plt.title('FIR Filter Impulse Response')
        plt.xlabel('Tap Index')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_snr_summary(snr_log_path: str, save_path: str) -> None:
        """
        Plot and save SNR (Signal-to-Noise Ratio) comparison bar chart.

        Parameters:
        - snr_log_path: Path to a JSON file containing SNR values in the format:
            {
                "segment_name": {"before": float, "after": float},
                ...
            }
        - save_path: Path to save the generated plot.
        """
        if not os.path.exists(snr_log_path):
            raise FileNotFoundError(f"SNR log file not found: {snr_log_path}")

        with open(snr_log_path, 'r') as file:
            snr_data = json.load(file)

        segments = list(snr_data.keys())
        snr_before = [snr_data[seg]["before"] for seg in segments]
        snr_after = [snr_data[seg]["after"] for seg in segments]

        x = np.arange(len(segments))
        width = 0.35

        plt.figure(figsize=(18, 5))
        plt.bar(x - width / 2, snr_before, width, label='Before', color='skyblue')
        plt.bar(x + width / 2, snr_after, width, label='After', color='orange')
        plt.xticks(x, segments, rotation=90)
        plt.xlabel('Segment')
        plt.ylabel('SNR (dB)')
        plt.title('SNR Comparison: Before vs After Filtering')
        plt.legend()
        plt.grid(axis='y', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()