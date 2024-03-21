import pyaudio
import numpy as np
import threading
volume = None
def getloudness():
    volume_event = threading.Event()

    audio = pyaudio.PyAudio()

    chunk_size = 1024
    sample_rate = 44100
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    running=True
    global volume
    while running:

        data = stream.read(chunk_size, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()
        volume_event.set()  

    stream.stop_stream()
    stream.close()
    audio.terminate()