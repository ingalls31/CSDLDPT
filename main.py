from audio import Sound
from features_extract import Init, Extract
from kdtree import CustomKDTree
import pickle
import os

# init = Init("audio")
# init.init()

# with open("sounds.obj", "rb") as s:
#     sounds = pickle.load(s)

# tree = CustomKDTree(sounds=sounds)

# extract = Extract(normalize_path="normalize.obj", sound_path="test_audio.mp3")
# vector = extract.features()

# query = Sound(features=vector, path="test_audio.mp3")
# result = tree.query_knn(sound_query=query, k=5)
# for path, dis in result:
#     print(f"{path} --> {dis}")

while True:
    query = input()
    if query == "exit": break
    elif query == "init":
        init = Init("audio")
        init.init()
    elif query.startswith("find "):
        file_path = query[5:]
        if not os.path.isfile("query/" + file_path): print(f"File {file_path} was not found.")
        else:
            with open("sounds.obj", "rb") as s:
                sounds = pickle.load(s)

            tree = CustomKDTree(sounds=sounds)

            extract = Extract(normalize_path="normalize.obj", sound_path="test_audio.mp3")
            vector = extract.features()

            query = Sound(features=vector, path="test_audio.mp3")
            result = tree.query_knn(sound_query=query, k=5)
            for path, dis in result:
                print(f"{path} --> {dis}")
    
    else: print("Query does not exist.")
