import librosa
import numpy as np

x, sr = librosa.load("data/Blackbird.mp3")

r = librosa.feature.spectral_rolloff(y=x, sr=sr)
print(r)

