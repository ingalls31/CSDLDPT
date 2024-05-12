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
    def __init__(self, path_to_sound_folder: str,
                 path_to_birds: str, path_to_query: str):
        self.path = path_to_sound_folder
        self.birds = path_to_birds
        self.query = path_to_query
    
    def features(self, path):
        x,sr = librosa.load(path) # sr : sample rate
        
        ave_energy = np.average(x*x) # năng lượng trung bình
        rms = librosa.feature.rms(y=x) # 
        zcr = librosa.feature.zero_crossing_rate(y=x) # tốc độ đổi dấu
        
        spec_cent = librosa.feature.spectral_centroid(y=x,sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=x,sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=x,sr=sr)
        
        vector = [ave_energy, np.mean(rms), np.mean(spec_cent), 
                np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]

        return vector
        
    def init(self):
        if os.path.exists(self.birds):
            print("Folder birds is not empty. Cleaning..")
            shutil.rmtree(self.birds)
        os.makedirs(self.birds)
        print("Clean up completed.")
        if os.path.exists(self.query):
            print("Folder query is not empty. Cleaning..")
            shutil.rmtree(self.query)
        os.makedirs(self.query)
        print("Clean up completed.")
        
        dataset = os.listdir(self.path)
        n_of_sample = len(dataset) * 4 // 5 # birds : query = 4 : 1
        audio = random.sample(dataset, n_of_sample)
        
        print("Moving audio file to folder birds..")
        for file in tqdm(audio, colour="yellow"):
            source = os.path.join(self.path, file)
            destination = os.path.join(self.birds, file)
            shutil.copyfile(source, destination)
        print("Moved completed.")

        print("Moving audio file to folder query..")
        for file in tqdm(dataset, colour="yellow"):
            if file not in audio:
                source = os.path.join(self.path, file)
                destination = os.path.join(self.query, file)
                shutil.copyfile(source, destination)
        print("Moved completed.")
        
        folder = os.listdir(self.birds)
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
    
    
