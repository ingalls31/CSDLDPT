import os

i=1
for root, dir, files in os.walk('audio'):
    for file in files:
        i+=1

print(i)