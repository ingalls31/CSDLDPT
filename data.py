import pickle

with open("sounds.obj", "rb") as f:
    sounds = pickle.load(f)
    
with open("data.txt","w") as f:   
    for i, s in enumerate(sounds):
        f.write(f"{s.path}:\n{s.features}\n")
