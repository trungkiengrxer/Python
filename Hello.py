import os

countImgFiles = 0;
for dirpath, dirnames, filenames in os.walk(r'D:\Downloads'):
    for filename in filenames:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            countImgFiles += 1
            print(os.path.join(dirpath, filename))

print(countImgFiles)
