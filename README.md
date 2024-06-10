### CSDLDPT
A basic system used to find k audio files with similar content in a directory.

### init
- Moves the sounds in "audio" folder into "birds" and "query" in a 4:1 ratio, extracts the audio's features in "birds" then saves it to "normalize.obj" in vector format, the list of sounds in "birds" is saved in "sound.obj"
```python
python init.py
```

### Run this program:
```python
python main.py
```

### Using query:
-<audio's name>: finds 5 files with similar features in "birds"
```python
#example
>test_audio.mp3
test1.mp3
test2.mp3
test3.mp3
```
- exit: quits the program
```python
>exit
```