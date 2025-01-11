import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the ECG data from the CSV file
file_path = 'data-100.csv'
ecg_data = pd.read_csv(file_path)

# Assuming the ECG signal is in the first column, named 'ECG' or similar
ecg_signal = ecg_data.iloc[:, 0].values

# Display the loaded ECG signal (full signal)
plt.figure(figsize=(10, 4))
plt.plot(ecg_signal)
plt.title('Original ECG Signal')
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')
plt.show()

# Set the level (threshold) for level crossing
threshold = 0.5 * np.max(ecg_signal)

# Find level crossings
crossings = np.where((ecg_signal[:-1] < threshold) & (ecg_signal[1:] >= threshold))[0]

# Extract peaks based on level crossings
r_peaks = []
fs = 360  # Sampling frequency in Hz
window_size = int(0.1 * fs)  # 100 ms window

for crossing in crossings:
    window_start = max(0, crossing - window_size)
    window_end = min(len(ecg_signal), crossing + window_size)
    peak_index = window_start + np.argmax(ecg_signal[window_start:window_end])
    r_peaks.append(peak_index)

r_peaks = np.array(r_peaks)

# Segment the ECG signal into 10-second segments
segment_duration = 10  # in seconds
samples_per_segment = segment_duration * fs
num_segments = int(np.ceil(len(ecg_signal) / samples_per_segment))

# Plot each segment with detected R-peaks
for i in range(num_segments):
    start_index = i * samples_per_segment
    end_index = min((i + 1) * samples_per_segment, len(ecg_signal))

    segment_signal = ecg_signal[start_index:end_index]
    segment_peaks = r_peaks[(r_peaks >= start_index) & (r_peaks < end_index)]

    # Adjust peak indices to segment's local index
    local_peaks = segment_peaks - start_index

    plt.figure(figsize=(10, 4))
    plt.plot(segment_signal, label='ECG Signal')
    plt.plot(local_peaks, segment_signal[local_peaks], 'ro', label='R-peaks')
    plt.axhline(y=threshold, color='g', linestyle='--', label='Threshold')
    plt.title(f'ECG Signal Segment {i + 1} with Detected R-peaks')
    plt.xlabel('Sample Number (within segment)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()