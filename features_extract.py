import librosa
import numpy as np
from audio import Sound
import pickle
from typing import List
from tqdm import tqdm
import os
import shutil
import random

class Init:
    def __init__(self, path_to_sound_folder: str):
        self.path = path_to_sound_folder
    
    def normalize(self, vector):
        # with open(self.normalize_path, 'rb') as input:
        #     min = pickle.load(input)
        #     max = pickle.load(input)
        #     vector = np.array(vector)
        
        min = np.min(vector)
        max = np.max(vector)
        
        return (vector-min) / (max-min)
    
    def features(self, path):
        x,sr = librosa.load(path) # sr : sample rate
        
        ave_energy = np.average(x*x) # năng lượng trung bình
        rms = librosa.feature.rms(y=x) # căn bậc 2 năng lượng trung bình trong từng frame 
        zcr = librosa.feature.zero_crossing_rate(y=x) # số lần tín hiệu đổi dấu
        
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        
        # vector = np.array([[ave_energy]*len(rms[0]), rms[0], zcr[0],
        #                    spec_cent[0], spec_bw[0], rolloff[0]])
        vector = np.array([[ave_energy]*len(rms[0]), self.normalize(rms[0]), self.normalize(zcr[0]),
                           self.normalize(spec_cent[0]), self.normalize(spec_bw[0]), self.normalize(rolloff[0])])

        return vector.T
        
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
        
        print("Saved normalize value at normalize.obj.")
        
        with open('sounds.obj', 'wb') as output:
            pickle.dump(sounds, output, pickle.HIGHEST_PROTOCOL)
        
        print("Saved sound's list at sounds.obj.")

class Extract:
    def __init__(self, normalize_path : str, sound_path : str):
        self.normalize_path = normalize_path # path to normalize file
        self.sound_path = sound_path # path to sound file
    
    def normalize(self, vector):
        # with open(self.normalize_path, 'rb') as input:
        #     min = pickle.load(input)
        #     max = pickle.load(input)
        #     vector = np.array(vector)
        
        min = np.min(vector)
        max = np.max(vector)
        
        return (vector-min) / (max-min)

    def features(self):
        x,sr = librosa.load(self.sound_path)   
        
        ave_energy = np.average(x*x)
        rms = librosa.feature.rms(y=x)
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y=x)
        
        vector = np.array([[ave_energy]*len(rms[0]), self.normalize(rms[0]), self.normalize(zcr[0]),
                           self.normalize(spec_cent[0]), self.normalize(spec_bw[0]), self.normalize(rolloff[0])])

        return vector.T
    
    
