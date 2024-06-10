from audio import Sound
from features_extract import Init, Extract
from kdtree import CustomKDTree, Queries
import pickle
import os

while True:
    query = input(">")
    if query == "exit": break
    elif query == "init":
        init = Init(path_to_sound_folder="audio")
        init.init()
        print()
    elif query.startswith("find "):
        file_path = "query/" + query[5:]
        if not os.path.isfile(file_path): print(f"File {file_path} was not found.")
        else:
            with open("sounds.obj", "rb") as s:
                sounds = pickle.load(s)

            queries = Queries(sounds=sounds)

            extract = Extract(normalize_path="normalize.obj", sound_path=file_path)
            vector = extract.features()
            q = Sound(features=vector, path=file_path)
            
            results = queries.query(input=q,k=3)
            for r in results:
                print(r)
            print()
    else: print("Query does not exist.\n")
