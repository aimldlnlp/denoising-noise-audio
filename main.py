import os
import pathlib
from signal_loader import SignalLoader
from frequency_analyzer import FrequencyAnalyzer
from visualization import SignalVisualizer

def main():
    audio_file_path = "dataset/seg_115.wav"
    base_results_dir = 'results'
    
    try:
        audio_filename = pathlib.Path(audio_file_path).stem
        results_dir = os.path.join(base_results_dir, audio_filename)
        os.makedirs(results_dir, exist_ok=True)
        
        # Load and normalize signal
        loader = SignalLoader(audio_file_path)
        signal, sample_rate = loader.load_signal()
        normalized_signal = loader.normalize_signal()
        
        # Frequency analysis
        analyzer = FrequencyAnalyzer(normalized_signal, sample_rate)
        dominant_frequencies = analyzer.identify_dominant_frequencies()
        noise_characteristics = analyzer.compute_noise_characteristics()
        
        # Define noise bands and design FIR filter
        noise_bands = [(49, 51), (98, 102), (30, 36)]
        fir_coeffs = analyzer.design_fir_filter(noise_bands)
        
        # Apply FIR filter
        filtered_signal = analyzer.apply_fir_filter(fir_coeffs)
        
        # Save filtered signal
        filtered_audio_path = os.path.join(results_dir, "filtered_audio.wav")
        loader.save_signal(filtered_signal, filtered_audio_path)
        
        # Visualize filter response
        SignalVisualizer.plot_filter_response(
            fir_coeffs, sample_rate, 
            save_path=os.path.join(results_dir, "filter_response.png")
        )
        
        print(f"\nFiltered audio saved to: {filtered_audio_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()