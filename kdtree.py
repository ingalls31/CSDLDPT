from scipy.spatial import KDTree
from typing import List
from audio import Sound

class CustomKDTree:
    def __init__(self, sounds: List[Sound]):
        self.sounds = sounds
        self.kd_tree = KDTree([sound.features for sound in sounds])
    
    def query_nn(self, sound_query: Sound):
        distance, index = self.kd_tree.query(sound_query.features)
        return self.sounds[index].path, distance
    
    def query_knn(self, sound_query: Sound, k: int):
        distances, indexes = self.kd_tree.query(sound_query.features, k)
        result = [(self.sounds[index].path, dist) for index, dist in zip(indexes, distances)]
        return result

