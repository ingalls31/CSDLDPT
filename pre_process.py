from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from tqdm import tqdm
import noisereduce as nr
import numpy as np

thresh = -35

for f in tqdm(os.listdir("data")):
    sound = AudioSegment.from_file("data/"+f)

    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=thresh) #dBMS

    if len(chunks) == 0: continue
    
    filtered_sound = chunks[0]
    for chunk in chunks[1:]:
        filtered_sound += chunk
    
    samples = np.array(filtered_sound.get_array_of_samples())
    reduced_noise = nr.reduce_noise(y=samples, sr=sound.frame_rate)
    
    output_audio = AudioSegment(reduced_noise.tobytes(), frame_rate=sound.frame_rate, sample_width=reduced_noise.dtype.itemsize, channels=1)
    
    output_audio.export("preprocess/"+f"{f[:-4]}.mp3", format="mp3")
