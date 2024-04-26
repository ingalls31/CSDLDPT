import librosa
import numpy as np
from audio import Sound
import pickle
from typing import List
from tqdm import tqdm
import os

class Init:
    def __init__(self, path_to_sound_folder: str):
        self.path = path_to_sound_folder
    
    def features(self, path):
        x,sr = librosa.load(path)   
        
        ave_energy = np.average(x*x)
        rms = librosa.feature.rms(y=x)
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y=x)
        
        vector = [ave_energy, np.mean(rms), np.mean(spec_cent), 
                np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
        
        return vector
        
    def init(self):
        folder = os.listdir(self.path)
        vectors = []
        sounds = []
        for file in tqdm(folder, colour="yellow"):
            sound_path = self.path + "/" + file
            vector = self.features(sound_path)
            vectors.append(vector)
            sound = Sound(vector, sound_path)
            sounds.append(sound)
        
        print("Extraction completed.")
            
        Min = np.vstack(vectors).min(axis=0)
        Max = np.vstack(vectors).max(axis=0)
        with open('normalize.obj', 'wb') as output:
            pickle.dump(Min, output, pickle.HIGHEST_PROTOCOL)
            pickle.dump(Max, output, pickle.HIGHEST_PROTOCOL)
        
        print("Saved normalize value.")
        
        with open('sounds.obj', 'wb') as output:
            pickle.dump(sounds, output, pickle.HIGHEST_PROTOCOL)
        
        print("Saved sound's list.")

class Extract:
    def __init__(self, normalize_path : str, sound_path : str):
        self.normalize_path = normalize_path # path to normalize file
        self.sound_path = sound_path # path to sound file
    
    def normalize(self, vector: List):
        with open(self.normalize_path, 'rb') as input:
            min = pickle.load(input)
            max = pickle.load(input)
            vector = np.array(vector)
        return (vector-min) / (max-min)

    def features(self):
        x,sr = librosa.load(self.sound_path)   
        
        ave_energy = np.average(x*x)
        rms = librosa.feature.rms(y=x)
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y=x)
        
        vector = [ave_energy, np.mean(rms), np.mean(spec_cent), 
                np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
        
        return vector
    
    
