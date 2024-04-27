### Run this program:
```python
python main.py
```
### Using query:
- init: moves the sounds in "audio" folder into "birds" and "query" in a 4:1 ratio, extracts the audio's features in "birds" then saves it to "normalize.obj" in vector format, the list of sounds in "birds" is saved in "sound.obj"
```python
>init
```
- find + <audio's name>: finds 5 files with similar features in "birds"
```python
#example
>find test_audio.mp3
```