import librosa
import numpy as np


y, sr = librosa.load("audio/Black Redstart_1.mp3")

# Tính toán phổ biên độ Fourier
D = np.abs(librosa.stft(y))

# Tính toán phổ biên độ trung bình trên các khung thời gian
S = np.mean(D, axis=1)

# Tìm chỉ số của tần số cao nhất
max_index = np.argmax(S)

# Tính toán tần số cao nhất tương ứng với chỉ số đó
frequencies = librosa.fft_frequencies(sr=sr)
max_frequency = frequencies[max_index]

print(f"{max_frequency} Hz")
