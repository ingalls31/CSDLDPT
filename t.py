import librosa
import numpy as np

x, sr = librosa.load("query/Redstart.mp3")

ave_energy = np.average(x*x)

print(ave_energy)
# rms = librosa.feature.rms(y=x)
# zcr = librosa.feature.zero_crossing_rate(y=x)

# spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
# spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
# rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)

# features = np.array([[ave_energy]*len(rms[0]), rms[0], zcr[0], spec_cent[0], spec_bw[0], rolloff[0]])

# print(features.shape)
# print(features)