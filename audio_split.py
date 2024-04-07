from pydub import AudioSegment
import os

def split_mp3(input_file, target_folder, split_length=10, max_splits=10):
    audio = AudioSegment.from_mp3(input_file)
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    total_length_seconds = len(audio) // 1000
    number_of_splits = min(max_splits, total_length_seconds // split_length)
    
    for i in range(number_of_splits):
        start_ms = i * split_length * 1000
        end_ms = start_ms + split_length * 1000
        
        split_audio = audio[start_ms:end_ms]
        
        split_filename = os.path.join(target_folder, f'{input_file[5:-4]}_{i+1}.mp3')
        split_audio.export(split_filename, format="mp3")
        
        print(f'Saved: {split_filename}')

    print('Splitting complete.')

def main(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)  # Đường dẫn đầy đủ của tệp MP3
                split_mp3(input_file=file_path, target_folder='audio')

main(folder='data')