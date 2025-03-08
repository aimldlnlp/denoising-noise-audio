# noise_analysis/main.py
import os
import pathlib
from signal_loader import SignalLoader
from frequency_analyzer import FrequencyAnalyzer
from visualization import SignalVisualizer

def main():
    # File path to your noise audio file
    audio_file_path = "dataset\seg_115.wav"
    
    # Base results directory
    base_results_dir = 'results'
    
    try:
        # Extract filename without extension
        audio_filename = pathlib.Path(audio_file_path).stem
        
        # Create a unique results subdirectory based on the audio filename
        results_dir = os.path.join(base_results_dir, audio_filename)
        
        # Ensure results directory exists
        os.makedirs(results_dir, exist_ok=True)
        
        # Load the signal
        loader = SignalLoader(audio_file_path)
        signal, sample_rate = loader.load_signal()
        
        # Normalize the signal
        normalized_signal = loader.normalize_signal()
        
        # Create frequency analyzer
        analyzer = FrequencyAnalyzer(normalized_signal, sample_rate)
        
        # Visualize time domain signal
        SignalVisualizer.plot_time_domain(
            normalized_signal, 
            sample_rate, 
            title=f'Time Domain Signal - {audio_filename}',
            save_path=os.path.join(results_dir, 'time_domain_signal.png')
        )
        
        # Compute and visualize frequency spectrum
        frequencies, magnitudes = analyzer.compute_fft()
        SignalVisualizer.plot_frequency_spectrum(
            frequencies, 
            magnitudes, 
            title=f'Frequency Spectrum - {audio_filename}',
            save_path=os.path.join(results_dir, 'frequency_spectrum.png')
        )
        
        # Compute and visualize power spectral density
        psd_frequencies, psd = analyzer.compute_power_spectral_density()
        SignalVisualizer.plot_power_spectral_density(
            psd_frequencies, 
            psd, 
            title=f'Power Spectral Density - {audio_filename}',
            save_path=os.path.join(results_dir, 'power_spectral_density.png')
        )
        
        # Identify dominant frequencies
        dominant_frequencies = analyzer.identify_dominant_frequencies()
        print("Dominant Frequencies:")
        for freq, mag in dominant_frequencies.items():
            print(f"Frequency: {freq:.2f} Hz, Magnitude: {mag:.2f}")
        
        # Compute noise characteristics
        noise_characteristics = analyzer.compute_noise_characteristics()
        print("\nNoise Characteristics:")
        for name, value in noise_characteristics.items():
            print(f"{name}: {value}")
        
        # Save analysis results to a text file
        results_file = SignalVisualizer.save_analysis_results(
            dominant_frequencies, 
            noise_characteristics, 
            results_dir
        )
        print(f"\nAnalysis results saved to: {results_dir}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()