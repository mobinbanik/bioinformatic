import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt

# خواندن داده‌های ECG از فایل
file_path = 'data.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# تبدیل داده‌ها به آرایه numpy
data = []
for line in lines:
    values = line.strip().split(',')
    data.extend([float(value) for value in values])
data = np.array(data)


# تابع برای فیلتر پایین‌گذر
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


# تابع برای فیلتر بالاگذر
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


# اعمال فیلتر پایین‌گذر
def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# اعمال فیلتر بالاگذر
def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# تنظیمات فیلتر
fs = 1000  # فرکانس نمونه‌برداری (فرض شده)
low_cutoff = 30  # فرکانس قطع پایین‌گذر (Hz)
high_cutoff = 1  # فرکانس قطع بالاگذر (Hz)

# اعمال فیلتر پایین‌گذر و بالاگذر
filtered_data = lowpass_filter(data, low_cutoff, fs)
filtered_data = highpass_filter(filtered_data, high_cutoff, fs)

# محاسبه مشتق مرتبه اول
derivative = np.diff(filtered_data)

# تقویت سیگنال با توان دو کردن
squared = derivative ** 2

# هموارسازی با استفاده از یک پنجره متحرک (moving average)
window_size = int(0.15 * fs)  # فرض کنیم پنجره هموارسازی 150 میلی‌ثانیه باشد
moving_average = np.convolve(squared, np.ones(window_size) / window_size, mode='same')

# شناسایی قله‌های R با تنظیمات مناسب
peaks, _ = find_peaks(moving_average, distance=200, height=np.mean(moving_average) * 2,
                      prominence=np.mean(moving_average) * 1.5)


# تابع برای نمایش سیگنال در بخش‌های کوچکتر
def plot_in_segments(data, peaks, segment_length):
    num_samples = len(data)
    num_segments = num_samples // segment_length + (1 if num_samples % segment_length != 0 else 0)

    for i in range(num_segments):
        start = i * segment_length
        end = min((i + 1) * segment_length, num_samples)

        plt.figure(figsize=(12, 4))
        print(data[start:end])
        plt.plot(data[start:end], label="ECG Signal Segment")
        segment_peaks = [p - start for p in peaks if start <= p < end]
        plt.plot(segment_peaks, data[start + np.array(segment_peaks)], "x", markersize=10, label="R Peaks")
        title = f"ECG Signal Segment {i + 1}"
        plt.title(title)
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()
        # plt.savefig(title, dpi=300)


# تنظیمات بخش‌بندی
segment_length = 200  # تعداد نمونه‌ها در هر بخش

# نمایش سیگنال در بخش‌های کوچکتر
plot_in_segments(data, peaks, segment_length)
