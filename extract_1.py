"""
Extract features with librosa's library
"""

import os
import numpy as np
import librosa
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

def extract(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        
        mfccs = librosa.feature.mfcc(y=y, sr=sr) 
        mfccs_processed = np.mean(mfccs.T,axis=0)
    except Exception as e:
        print("Error")
        mfccs_processed = None
    return mfccs_processed

def load_dataset(audio_dir):
    features = []
    file_paths = []
    
    print("Loading dataset..")
    for file in tqdm(os.listdir(audio_dir)):
        if file.endswith(".mp3"):
            file_path = os.path.join(audio_dir, file)
            mfccs = extract(file_path)
            
            if mfccs is None:
                continue
            
            features.append(mfccs)
            file_paths.append(file_path)
    print("Completed!")
    
    return np.array(features), file_paths

def find(input_audio_path, audio_dir):
    input_features = extract(input_audio_path)
    
    dataset_features, file_paths = load_dataset(audio_dir)
    
    model = NearestNeighbors(n_neighbors=10)
    model.fit(dataset_features)
    
    d, indices = model.kneighbors([input_features]) # d means distances
    # closest_index = indices[0][0]
    # closest_file_path = file_paths[closest_index]
    
    print(f"input: {input_audio_path}\nResult:")    
    for i in range(0, len(d.flatten())):
        # if i == 0:
        #     pass
        # else:
        print(f"{i+1}: {file_paths[indices.flatten()[i]]}") #, Khoảng cách: {d.flatten()[i]}")

    
    # print(f"Results: {closest_file_path}")

find('test_audio.mp3', 'audio/')