import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf
import json


class EnhancedSignalVisualizer:

    @staticmethod
    def plot_time_domain(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str):
        times = np.arange(len(before)) / sample_rate
        plt.figure(figsize=(14, 4))
        plt.plot(times, before, label='Original', alpha=0.6)
        plt.plot(times, after, label='Filtered', alpha=0.8)
        plt.title('Time Domain Signal (Before vs After)')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_frequency_spectrum(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str):
        def compute_fft(signal_data):
            freqs = np.fft.rfftfreq(len(signal_data), d=1/sample_rate)
            fft_vals = np.abs(np.fft.rfft(signal_data))
            return freqs, fft_vals

        freqs_before, fft_before = compute_fft(before)
        freqs_after, fft_after = compute_fft(after)

        plt.figure(figsize=(14, 4))
        plt.plot(freqs_before, fft_before, label='Original', alpha=0.6)
        plt.plot(freqs_after, fft_after, label='Filtered', alpha=0.8)
        plt.title('Frequency Spectrum (FFT)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_psd(before: np.ndarray, after: np.ndarray, sample_rate: int, save_path: str):
        f_before, Pxx_before = signal.welch(before, fs=sample_rate, nperseg=1024)
        f_after, Pxx_after = signal.welch(after, fs=sample_rate, nperseg=1024)

        plt.figure(figsize=(14, 4))
        plt.semilogy(f_before, Pxx_before, label='Original', alpha=0.6)
        plt.semilogy(f_after, Pxx_after, label='Filtered', alpha=0.8)
        plt.title('Power Spectral Density (Welch)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_filter_kernel(fir_coeffs: np.ndarray, save_path: str):
        plt.figure(figsize=(10, 3))
        plt.stem(fir_coeffs, use_line_collection=True)
        plt.title('FIR Filter Impulse Response')
        plt.xlabel('Tap Index')
        plt.ylabel('Amplitude')
        plt.grid()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_snr_summary(snr_log_path: str, save_path: str):
        """
        snr_log_path should point to a JSON or CSV file of this format:
        {
            "seg_1": {"before": 20.1, "after": 26.4},
            "seg_2": {"before": 15.7, "after": 23.0},
            ...
        }
        """
        with open(snr_log_path, 'r') as f:
            snr_data = json.load(f)

        segments = list(snr_data.keys())
        snr_before = [snr_data[seg]["before"] for seg in segments]
        snr_after = [snr_data[seg]["after"] for seg in segments]

        x = np.arange(len(segments))
        width = 0.35

        plt.figure(figsize=(18, 5))
        plt.bar(x - width/2, snr_before, width, label='Before')
        plt.bar(x + width/2, snr_after, width, label='After')
        plt.xticks(x, segments, rotation=90)
        plt.xlabel('Segment')
        plt.ylabel('SNR (dB)')
        plt.title('SNR Before vs After Filtering')
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()