import pyaudio
import numpy as np
import threading
import program
import os
volume = None
def getloudness():
    current_selected_device=["defaul", -1]
    volume_event = threading.Event()

    audio = pyaudio.PyAudio()
    devfile=os.path.exists("devfile.txt")
    for i in range(audio.get_device_count()):
        device=audio.get_device_info_by_index(i)
        if devfile:
            open("devfile.txt", "a").write(str(audio.get_device_info_by_index(i))+"\n\n")
        if not device["maxInputChannels"] > 0 or not device["hostApi"]==1:
            continue
        if not device["name"] in program.audio_devices.device_dict:
            program.audio_devices.device_dict[device["name"]]=i
            program.audio_devices.device_list.append(device["name"])
    
    chunk_size = 1024
    sample_rate = 44100
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
    running=True
    global volume
    while running:
        if not current_selected_device==program.audio_devices.selected_device:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            del audio
            del stream
            audio = pyaudio.PyAudio()
            current_selected_device=program.audio_devices.selected_device
            chunk_size = 1024
            sample_rate = 44100
            if not program.audio_devices.selected_device[1]==-1:
                try:
                    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size,input_device_index=current_selected_device[1])
                except:
                    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
            else:
                stream = audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
        data = stream.read(chunk_size, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()
        volume_event.set()

    stream.stop_stream()
    stream.close()
    audio.terminate()