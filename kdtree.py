from scipy.spatial import KDTree
from typing import List
from audio import Sound
from tqdm import tqdm
import numpy as np

class CustomKDTree:
    def __init__(self, sounds: List[Sound]):
        self.sounds = sounds
        self.kd_tree = KDTree([sound.features for sound in sounds])
    
    def query_nn(self, sound_query: Sound):
        distance, index = self.kd_tree.query(sound_query.features)
        return self.sounds[index].path, distance
    
    def query_knn(self, sound_query: Sound, k: int): # k nearest neighbor
        distances, indexes = self.kd_tree.query(sound_query.features, k)
        result = [(self.sounds[index].path, dist) for index, dist in zip(indexes, distances)]
        return result

class Queries:
    def __init__(self, sounds: List[Sound]):
        self.sounds = sounds
    
    def dis(self, vec1, vec2):
        return np.sum(np.abs(vec1-vec2))
    
    def query(self, input: Sound, k: int):
        similarity = {}
        for sound in self.sounds:
            feaW = input.features # input's features, W means "window", using to slide
            feaS = sound.features # sound's features
            if len(feaW) > len(feaS): feaW, feaS = feaS, feaW # make sure that vector with smaller size will slide over another
            
            '''
                Slide feaW over feaS
            '''
            
            overlap = int(0.2 * len(feaW))
            steps = (len(feaS)-len(feaW)) // overlap + 1
            vector = np.zeros(steps)
            
            for i in range(steps):
                '''
                per segment
                '''
                iS = i * overlap    # start index
                iE = iS + len(feaW) # end index
                fea_temp = feaS[iS:iE]
                vec_temp = np.zeros(len(feaW))
                
                for f in range(len(feaW)):
                    '''
                    per features vector6
                    '''
                    vec_temp[f] = self.dis(feaW[f], fea_temp[f])
                vector[i] = np.median(vec_temp)
                
            similarity[sound.path] = np.min(vector) # take median of features vector
        
        sorted_similarity = sorted(similarity.items(), key=lambda item: item[1])
        return [item[0] for item in sorted_similarity[:k]]
        