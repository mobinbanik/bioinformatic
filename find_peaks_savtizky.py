import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# خواندن داده‌های ECG از فایل
file_path = 'extracted_data/data-100.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# تبدیل داده‌ها به آرایه numpy
data = []
for line in lines:
    values = line.strip().split(',')
    data.extend([float(value) for value in values])
data = np.array(data)

# اعمال فیلتر Savitzky-Golay برای هموارسازی داده‌های اصلی
window_length = 101  # طول پنجره (باید فرد باشد)
polyorder = 3  # درجه چندجمله‌ای

# هموارسازی سیگنال اصلی
smoothed_data = savgol_filter(data, window_length=window_length, polyorder=polyorder)

# شناسایی قله‌های R در سیگنال هموار شده
peaks, _ = find_peaks(smoothed_data, distance=200, height=np.mean(smoothed_data) * 2,
                      prominence=np.mean(smoothed_data) * 1.5)


# تابع برای نمایش سیگنال در بخش‌های کوچکتر
def plot_in_segments(data, peaks, segment_length):
    num_samples = len(data)
    num_segments = num_samples // segment_length + (1 if num_samples % segment_length != 0 else 0)

    for i in range(num_segments):
        start = i * segment_length
        end = min((i + 1) * segment_length, num_samples)

        plt.figure(figsize=(12, 4))
        plt.plot(data[start:end], label="Smoothed ECG Signal Segment")
        segment_peaks = [p - start for p in peaks if start <= p < end]
        plt.plot(segment_peaks, data[start + np.array(segment_peaks)], "x", label="R Peaks")
        plt.title(f"ECG Signal Segment {i + 1}")
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()


# تنظیمات بخش‌بندی
segment_length = 1000  # تعداد نمونه‌ها در هر بخش

# نمایش سیگنال هموار شده در بخش‌های کوچکتر
plot_in_segments(smoothed_data, peaks, segment_length)