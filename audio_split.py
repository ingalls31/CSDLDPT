from pydub import AudioSegment
import os
from tqdm import tqdm

len_audio = 1000 # ms

def split_mp3(input_file, audio_folder, query_folder, split_length=5):
    audio = AudioSegment.from_mp3(input_file)
    
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
        
    if not os.path.exists(query_folder):
        os.makedirs(query_folder)
    
    max_splits = (len(audio) // len_audio) // split_length    
    n_splits = int(max_splits * 0.7) # 70% for audio, 30% for query
    split_length *= len_audio
    
    for i in tqdm(range(n_splits)):
        start_ms = i * split_length
        end_ms = start_ms + split_length
        
        split_audio = audio[start_ms:end_ms]
        
        split_filename = os.path.join(audio_folder, f'{os.path.basename(input_file)[:-4]}_{i+1}.mp3')
        split_audio.export(split_filename, format="mp3")
        
        print(f'Saved: {split_filename}')

    
        
    split_audio = audio[n_splits*split_length:]
    
    split_filename = os.path.join(query_folder, f'{os.path.basename(input_file)[:-4]}.mp3')
    split_audio.export(split_filename, format="mp3")
    
    print(f'Saved: {split_filename}')
    
    print('Splitting complete.')

def main(folder, audio, query):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)  # Đường dẫn đầy đủ của tệp MP3
                split_mp3(input_file=file_path, audio_folder=audio, query_folder=query)

main(folder='preprocess', audio="audio", query='query')