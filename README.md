# Audio Denoising Using FIR Filtering

This project demonstrates an audio denoising pipeline, where noisy audio signals are processed using a custom FIR filter to remove specific frequency bands. The pipeline also includes visualization tools to compare the raw and filtered signals in time and frequency domains, as well as performance evaluation using Signal-to-Noise Ratio (SNR) and Spectral Flatness metrics.

## Project Structure

denoising_audio/
│
├── README.md
├── main.py
├── requirements.txt
├── signal_loader.py
├── signal_processing.py
├── visualization.py
│
├── dataset/ (contains .wav audio files)
├── evaluation/ (contains evaluation scripts)
├── results/ (contains analysis results per segment)
└── visualization/ (contains visualization scripts and outputs)


## Features

- **Noise Removal**: The project identifies and removes noise from audio signals using a custom-designed FIR filter.
- **Frequency Analysis**: It performs Fast Fourier Transform (FFT) and Power Spectral Density (PSD) analysis to identify noise characteristics.
- **Visualization**: Visualizes the time-domain waveform, frequency spectrum, and PSD of both raw and filtered audio signals.
- **Evaluation**: Computes Signal-to-Noise Ratio (SNR) and Spectral Flatness to evaluate the effectiveness of the filtering process.

## Requirements

- Python 3.x
- `numpy`
- `scipy`
- `soundfile`
- `matplotlib`

You can install the required dependencies by running:

```bash
pip install -r requirements.txt

# How to Use

1. **Prepare Your Dataset**: Place your noisy audio files in the `dataset/` directory. The files should be in `.wav` format.

2. **Run the Pipeline**:
   
   * The main script `main.py` loads an audio file, applies FIR filtering to remove noise, and saves the filtered audio in the `results/` directory.
   
   * You can specify the audio file path in the `main.py` script by modifying the `audio_file_path` variable.

3. **Visualize the Results**:
   
   * The `visualization/usage.py` script generates time-domain and frequency-domain visualizations comparing the original and filtered signals for a single audio segment.
   
   * The `visualization/batch_visualize.py` script can be used to generate visualizations for all the audio segments in the `dataset/` directory.

4. **Evaluate the Performance**:
   
   * The `evaluation/eval.py` script calculates the Signal-to-Noise Ratio (SNR) and Spectral Flatness for a pair of noisy and filtered signals.

## Code Description

### `main.py`

The entry point for the audio denoising pipeline. It loads an audio file, normalizes the signal, identifies noise characteristics, designs an FIR filter to remove noise, and saves the filtered audio.

### `signal_loader.py`

Responsible for loading, normalizing, and saving audio signals. It uses the `soundfile` library to read and write `.wav` files.

### `signal_processing.py`

Contains the `FrequencyAnalyzer` class, which performs:

*   FFT for frequency domain analysis
*   Power Spectral Density (PSD) calculation
*   Design and application of an FIR filter to remove noise

### `visualization/`

Contains functions to visualize the signals:

*   `EnhancedSignalVisualizer`: Provides static methods to plot time-domain waveforms, frequency spectrum, and PSD.
*   `batch_visualize.py`: A script to generate visualizations for all audio segments in the `dataset/` directory.
*   `usage.py`: A script to generate visualizations for a single audio segment.

### `evaluation/eval.py`

Calculates and displays the Signal-to-Noise Ratio (SNR) and Spectral Flatness between the original noisy and filtered audio signals.

## Future Improvements

*   **Machine Learning-based Denoising**: Implement machine learning models to learn noise profiles and remove noise more effectively.
*   **Multi-band FIR Filtering**: Use adaptive or multi-band FIR filtering to handle more complex noise types.
*   **Web Interface**: Create a web application for interactive audio denoising and visualization.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""