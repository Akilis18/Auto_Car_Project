import os
from pydub import AudioSegment

folder = r'/content/drive/MyDrive/samples'
files = os.listdir(folder)
for file in files:
    if file.endswith(".m4a"):
        m4a_file = folder + "/" + file
        wav_filename = os.path.join(folder, file.replace(".m4a", ".wav"))

        sound = AudioSegment.from_file(m4a_file, format='m4a')
        sound.export(wav_filename, format='wav')

# Move files
folder_old = r'/content/drive/MyDrive/samples'
folder_new = r'/content/drive/MyDrive/samples/raw/6'
files = os.listdir(folder_old)
for file in files:
    if file.endswith(".m4a"):
        old_path = folder_old + "/" + file
        new_path = folder_new + "/" + file
        os.rename(old_path, new_path)
