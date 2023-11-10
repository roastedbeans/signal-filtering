import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import soundfile as sf

# Load audio file
filename = 'snore1.wav'
data, sr = sf.read(filename)


# Plot original signal
plt.figure(figsize=(12,4))
plt.plot(data)
plt.title('Original Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Perform FFT
fft_data = np.fft.rfft(data)

# Compute PSD
psd_data = np.abs(fft_data)**2 / len(data)

# Set noise frequency band
noise_start = 50 # start of noise frequency band in Hz
noise_end = 1300 # end of noise frequency band in Hz

# Find indices of noise frequencies
freqs = np.fft.rfftfreq(len(data), d=1/sr)
noise_indices = np.where((freqs >= noise_start) & (freqs <= noise_end))[0]

# Apply notch filter to noise frequencies
notch_filter = np.ones(len(psd_data))
notch_filter[noise_indices] = 0
filtered_psd_data = psd_data * notch_filter

# Plot PSD before and after filtering
plt.figure(figsize=(12,4))
plt.plot(freqs, psd_data, label='Before Filtering')
plt.plot(freqs, filtered_psd_data, label='After Filtering')
plt.title('Power Spectral Density')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.legend()

# Apply inverse FFT to get filtered signal
filtered_data = np.fft.irfft(fft_data * notch_filter)

# Plot filtered signal
plt.figure(figsize=(12,4))
plt.plot(filtered_data)
plt.title('Filtered Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()

# Export filtered audio file
sf.write('audio_filtered.wav', filtered_data, sr)
