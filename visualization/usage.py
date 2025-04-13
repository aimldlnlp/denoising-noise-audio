from enhanced_visualization import EnhancedSignalVisualizer
import soundfile as sf
import json
import os

signal_path = 'dataset/seg_1.wav'
filtered_path = 'results/seg_1/filtered_audio.wav'
output_dir = 'final_visualization/seg_1'

os.makedirs(output_dir, exist_ok=True)

# Load audio
signal, sr = sf.read(signal_path)
filtered, _ = sf.read(filtered_path)

# Plot visuals
EnhancedSignalVisualizer.plot_time_domain(signal, filtered, sr, f"{output_dir}/time_domain_signal.png")
EnhancedSignalVisualizer.plot_frequency_spectrum(signal, filtered, sr, f"{output_dir}/frequency_spectrum.png")
EnhancedSignalVisualizer.plot_psd(signal, filtered, sr, f"{output_dir}/power_spectral_density.png")

# Optional filter kernel plot
# fir_coeffs = ... load or compute from pipeline
# EnhancedSignalVisualizer.plot_filter_kernel(fir_coeffs, f"{output_dir}/filter_response.png")

# Optional SNR summary (if you log per-segment)
# EnhancedSignalVisualizer.plot_snr_summary("results/snr_summary.json", "results/snr_chart.png")