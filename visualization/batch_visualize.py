import os
import glob
import soundfile as sf
from enhanced_visualization import EnhancedSignalVisualizer

# Paths
dataset_dir = 'dataset'
results_dir = 'results'
output_base_dir = 'final_visualization'

# List all original audio segments
audio_files = sorted(glob.glob(os.path.join(dataset_dir, 'seg_*.wav')))

for audio_path in audio_files:
    segment_name = os.path.splitext(os.path.basename(audio_path))[0]
    filtered_path = os.path.join(results_dir, segment_name, 'filtered_audio.wav')
    output_dir = os.path.join(output_base_dir, segment_name)

    try:
        # Make sure filtered audio exists
        if not os.path.exists(filtered_path):
            print(f"[!] Skipping {segment_name}: filtered audio not found.")
            continue

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Load signals
        raw_signal, sr = sf.read(audio_path)
        filtered_signal, _ = sf.read(filtered_path)

        # Plot and save visualizations
        EnhancedSignalVisualizer.plot_time_domain(raw_signal, filtered_signal, sr, os.path.join(output_dir, 'time_domain_signal.png'))
        EnhancedSignalVisualizer.plot_frequency_spectrum(raw_signal, filtered_signal, sr, os.path.join(output_dir, 'frequency_spectrum.png'))
        EnhancedSignalVisualizer.plot_psd(raw_signal, filtered_signal, sr, os.path.join(output_dir, 'power_spectral_density.png'))

        print(f"[✓] Visualizations saved for {segment_name}")

    except Exception as e:
        print(f"[X] Error processing {segment_name}: {e}")