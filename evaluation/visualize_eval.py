import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Load the evaluation summary
with open("evaluation/eval_summary.json", "r") as f:
    summary = json.load(f)

output_dir = "evaluation/plots2"
os.makedirs(output_dir, exist_ok=True)

# Helper to extract segment order
segments = sorted(summary.keys(), key=lambda x: int(x.split("_")[1]))

# -------- SNR Plot --------
snr_before = [summary[seg]["snr_before"] for seg in segments]
snr_after = [summary[seg]["snr_after"] for seg in segments]

x = np.arange(len(segments))
plt.figure(figsize=(14, 5))
plt.bar(x - 0.2, snr_before, width=0.4, label="Before", color="tomato")
plt.bar(x + 0.2, snr_after, width=0.4, label="After", color="seagreen")
plt.xticks(x, segments, rotation=90, fontsize=6)
plt.ylabel("SNR (dB)")
plt.title("Signal-to-Noise Ratio (Before vs After)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/snr_comparison.png")
plt.close()

# -------- Spectral Flatness Plot --------
flat_before = [summary[seg]["spectral_flatness_before"] for seg in segments]
flat_after = [summary[seg]["spectral_flatness_after"] for seg in segments]

plt.figure(figsize=(14, 5))
plt.plot(segments, flat_before, label="Before", marker='o', color='steelblue')
plt.plot(segments, flat_after, label="After", marker='x', color='orange')
plt.xticks(rotation=90, fontsize=6)
plt.ylabel("Spectral Flatness")
plt.title("Spectral Flatness (Before vs After)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/spectral_flatness.png")
plt.close()

# -------- Band Energy Reduction --------
# Average reduction per band
band_labels = list(next(iter(summary.values()))["band_energy"].keys())
reductions = {band: [] for band in band_labels}

for seg in segments:
    for band in band_labels:
        energy_before = summary[seg]["band_energy"][band]["before"]
        energy_after = summary[seg]["band_energy"][band]["after"]
        reduction = energy_before - energy_after
        reductions[band].append(reduction)

avg_reduction = {band: np.mean(vals) for band, vals in reductions.items()}

# Bar chart of avg reduction
plt.figure(figsize=(10, 5))
plt.bar(avg_reduction.keys(), avg_reduction.values(), color="slateblue")
plt.ylabel("Avg Energy Reduction (band PSD)")
plt.title("Average Band Energy Reduction Across Segments")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{output_dir}/band_energy_reduction.png")
plt.close()

# -------- Line Plots: Band Energy Per Segment --------
for band in band_labels:
    energy_before = [summary[seg]["band_energy"][band]["before"] for seg in segments]
    energy_after = [summary[seg]["band_energy"][band]["after"] for seg in segments]

    plt.figure(figsize=(14, 5))
    plt.plot(segments, energy_before, label="Before", marker='o', linestyle='-', color="crimson")
    plt.plot(segments, energy_after, label="After", marker='x', linestyle='--', color="forestgreen")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("Band Energy (PSD)")
    plt.title(f"Band Energy Over Segments - {band} Hz")
    plt.legend()
    plt.tight_layout()
    filename = band.replace("-", "_")
    plt.savefig(f"{output_dir}/band_energy_{filename}.png")
    plt.close()

print(f"[✓] Plots saved to: {output_dir}")