# from audio import Sound
# from features_extract import Init, Extract
# from kdtree import CustomKDTree
# import pickle
# import os

# while True:
#     query = input(">")
#     if query == "exit": break
#     elif query == "init":
#         init = Init(path_to_sound_folder="audio",
#                     path_to_birds="birds",
#                     path_to_query="query")
#         init.init()
#     elif query.startswith("find "):
#         file_path = "query/" + query[5:]
#         if not os.path.isfile(file_path): print(f"File {file_path} was not found.")
#         else:
#             with open("sounds.obj", "rb") as s:
#                 sounds = pickle.load(s)

#             tree = CustomKDTree(sounds=sounds)

#             extract = Extract(normalize_path="normalize.obj", sound_path=file_path)
#             vector = extract.features()

#             query = Sound(features=vector, path=file_path)
#             result = tree.query_knn(sound_query=query, k=5)
#             for path, dis in result:
#                 print(f"{path} --> {dis}")
    
#     else: print("Query does not exist.")

import os

i = 0
for f in os.listdir("audio"):
    i+=1
    
print(i)