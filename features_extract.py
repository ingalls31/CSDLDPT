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
        sounds = []
        for file in tqdm(folder, colour="yellow"):
            sound_path = self.path + "/" + file
            vector = self.features(sound_path)
            sound = Sound(vector, sound_path)
            sounds.append(sound)
        
        print("Extraction completed.")
        
        with open('sounds.obj', 'wb') as output:
            pickle.dump(sounds, output, pickle.HIGHEST_PROTOCOL)
        
        print("Saved sound's list at sounds.obj.")

class Extract:
    def __init__(self, sound_path : str):
        self.sound_path = sound_path # path to sound file
    
    def normalize(self, vector):
        min = np.min(vector)
        max = np.max(vector)
        
        return (vector-min) / (max-min)

    def features(self):
        x,sr = librosa.load(self.sound_path)   
        
        ave_energy = np.average(x*x) 
        # tổng bình phương giá trị tin hiệu chia cho tổng số mẫu
        rms = librosa.feature.rms(y=x) 
        # căn bậc hai của tổng bình phương của các giá trị tín hiệu chia cho tổng số mẫu
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr) 
        # tổng của (tần số f * biên độ của phổ) / tổng biên độ của phổ
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr) 
        # căn bậc hai [ tổng bình phương chênh lệch của tần số với tần số trung tâm * giá trị phổ tại 1 frame  / tổng các giá trị phổ ]
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        # tỉ lệ phần trăm tương ứng nhân tổng bình phương các năng lượng tại tần số
        zcr = librosa.feature.zero_crossing_rate(y=x) 
        #(1/2)*(1/N)*∑(n=1 to N-1)|sign[x(n)] - sign[x(n-1)]|
        
        vector = np.array([[ave_energy]*len(rms[0]), self.normalize(rms[0]), self.normalize(zcr[0]),
                           self.normalize(spec_cent[0]), self.normalize(spec_bw[0]), self.normalize(rolloff[0])])

        return vector.T
    
    
