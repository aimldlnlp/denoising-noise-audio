import os
import json
import glob
import soundfile as sf
from metrics import compute_snr, compute_spectral_flatness, compute_band_energy

# Settings
dataset_dir = 'dataset'
results_dir = 'results'
output_json = 'evaluation/eval_summary.json'
noise_bands = [(48, 51), (84, 87), (99, 101), (1196, 1199)]

# Prepare output
os.makedirs("evaluation", exist_ok=True)
summary = {}

# Process each segment
for original_path in sorted(glob.glob(f"{dataset_dir}/seg_*.wav")):
    seg_name = os.path.splitext(os.path.basename(original_path))[0]
    filtered_path = os.path.join(results_dir, seg_name, 'filtered_audio.wav')

    if not os.path.exists(filtered_path):
        print(f"[!] Skipping {seg_name} (filtered file not found)")
        continue

    # Load signals
    signal, sr = sf.read(original_path)
    filtered, _ = sf.read(filtered_path)
    
    # Align lengths
    min_len = min(len(signal), len(filtered))
    signal = signal[:min_len]
    filtered = filtered[:min_len]

    # SNR
    noise_before = signal - filtered  # Approximation (residual = noise)
    snr_before = compute_snr(signal, noise_before)
    snr_after = compute_snr(filtered, signal - filtered)

    # Spectral Flatness
    flat_before = compute_spectral_flatness(signal, sr)
    flat_after = compute_spectral_flatness(filtered, sr)

    # Band Energy Reductions
    band_energy_reduction = {
        f"{low}-{high}Hz": {
            "before": compute_band_energy(signal, sr, (low, high)),
            "after": compute_band_energy(filtered, sr, (low, high))
        } for (low, high) in noise_bands
    }

    summary[seg_name] = {
        "snr_before": snr_before,
        "snr_after": snr_after,
        "spectral_flatness_before": flat_before,
        "spectral_flatness_after": flat_after,
        "band_energy": band_energy_reduction
    }

    print(f"[✓] Evaluated {seg_name}")

# Save results
with open(output_json, "w") as f:
    json.dump(summary, f, indent=2)
print(f"\n[✓] Evaluation summary saved to {output_json}")