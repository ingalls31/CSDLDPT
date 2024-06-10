from audio import Sound
from features_extract import Init, Extract
from kdtree import CustomKDTree, Queries
import pickle
import os

init = Init(path_to_sound_folder="audio")
init.init()