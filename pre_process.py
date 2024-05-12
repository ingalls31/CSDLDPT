from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from tqdm import tqdm

for f in tqdm(os.listdir("data")):
    print(f[:-4])
    sound = AudioSegment.from_file("data/"+f)

    chunks = split_on_silence(sound, min_silence_len=1000, silence_thresh=-40)

    filtered_sound = chunks[0]
    for chunk in chunks[1:]:
        filtered_sound += chunk
    filtered_sound.export("preprocess/"+f"{f[:-4]}.mp3", format="mp3")
