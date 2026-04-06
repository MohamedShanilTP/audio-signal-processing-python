import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt

# Load audio files
quiet_audio, sr = librosa.load("quiet.wav", sr=16000)
noisy_audio, sr = librosa.load("noisy.wav", sr=16000)

# Normalize signals
quiet_audio = quiet_audio / np.max(np.abs(quiet_audio))
noisy_audio = noisy_audio / np.max(np.abs(noisy_audio))

# Match lengths
min_len = min(len(quiet_audio), len(noisy_audio))
quiet_audio = quiet_audio[:min_len]
noisy_audio = noisy_audio[:min_len]

# -------------------------
# Time Domain Plot
# -------------------------
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(quiet_audio)
plt.title("Quiet Audio - Time Domain")

plt.subplot(1, 2, 2)
plt.plot(noisy_audio)
plt.title("Noisy Audio - Time Domain")

plt.tight_layout()
plt.show()

# -------------------------
# FFT Analysis
# -------------------------
quiet_windowed = quiet_audio * np.hamming(len(quiet_audio))
noisy_windowed = noisy_audio * np.hamming(len(noisy_audio))

X_quiet = np.fft.fft(quiet_windowed)
X_noisy = np.fft.fft(noisy_windowed)

freqs = np.fft.fftfreq(len(X_noisy), 1/sr)

# Plot Frequency Spectrum
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(freqs[:len(freqs)//2], np.abs(X_quiet[:len(freqs)//2]))
plt.title("Quiet Audio - Frequency Spectrum")

plt.subplot(1, 2, 2)
plt.plot(freqs[:len(freqs)//2], np.abs(X_noisy[:len(freqs)//2]))
plt.title("Noisy Audio - Frequency Spectrum")

plt.tight_layout()
plt.show()

# -------------------------
# Frequency Filtering
# -------------------------
X_filtered = X_noisy.copy()
X_filtered[(freqs < 100) | (freqs > 3000)] = 0

# Inverse FFT
filtered_audio = np.fft.ifft(X_filtered)
filtered_audio = np.real(filtered_audio)

# Normalize
filtered_audio = filtered_audio / np.max(np.abs(filtered_audio))

# Save output
sf.write("filtered_output.wav", filtered_audio, sr)

# -------------------------
# Comparison Plot
# -------------------------
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(noisy_audio)
plt.title("Original Noisy Audio")

plt.subplot(1, 2, 2)
plt.plot(filtered_audio)
plt.title("Filtered Audio")

plt.tight_layout()
plt.show()
