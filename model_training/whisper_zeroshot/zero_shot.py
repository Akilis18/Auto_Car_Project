import whisper
import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import curses

def record_audio(duration=5, fs=16000, save_dir="recordings", remove_after_process=False):
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    # Generate a unique filename
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    file_path = os.path.join(save_dir, filename)
    wav.write(file_path, fs, audio)
    print(f"Audio recorded to {file_path}")
    return file_path, remove_after_process

def transcribe_audio_file(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language="zh")
    print("=== Transcribed Text ===")
    print(result["text"])
    return result["text"]

def transcribe_directory(directory, output_txt):
    model = whisper.load_model("small")
    with open(output_txt, "w", encoding="utf-8") as out_f:
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                audio_path = os.path.join(directory, filename)
                print(f"Transcribing {audio_path} ...")
                result = model.transcribe(audio_path, language="zh")
                out_f.write(f"{filename}: {result['text']}\n")

def main(stdscr):
    # Curses setup
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'q' to quit. Recording and detecting keywords...")
    stdscr.refresh()

    # Define keyword-to-sentence mapping
    keyword_map = {
        "後退": "Detected: Move backward",
        "前進": "Detected: Move forward",
        "左轉": "Detected: Turn left",
        "右轉": "Detected: Turn right",
        "停止": "Detected: Stop",
        # Add more keywords and sentences as needed
    }

    remove_audio = True  # Set to True to remove audio after processing, False to keep
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Press 'q' to quit. Recording and detecting keywords...")
        stdscr.addstr(2, 0, "Recording for 3 seconds...")
        stdscr.refresh()
        audio_path, _ = record_audio(duration=3, fs=16000, remove_after_process=remove_audio)
        transcribed_text = transcribe_audio_file(audio_path)

        found = False
        for keyword, sentence in keyword_map.items():
            if keyword in transcribed_text:
                stdscr.addstr(4, 0, sentence + " " * 40)
                found = True
                break
        if not found:
            stdscr.addstr(4, 0, "No known command detected." + " " * 40)
        stdscr.refresh()

        # Remove audio file if requested
        if remove_audio and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception as e:
                stdscr.addstr(6, 0, f"Error removing file: {e}" + " " * 20)
                stdscr.refresh()

        # Check for 'q' key press
        stdscr.addstr(5, 0, "Press 'q' to quit or wait for next recording..." + " " * 20)
        stdscr.refresh()
        for _ in range(10):  # Check for key press every 0.5s for 5s
            key = stdscr.getch()
            if key == ord('q'):
                stdscr.addstr(7, 0, "Exiting..." + " " * 20)
                stdscr.refresh()
                curses.napms(1000)
                return
            curses.napms(500)

if __name__ == "__main__":
    curses.wrapper(main)
