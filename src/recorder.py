import wave
import datetime
import numpy as np

class WavRecorder:
    def __init__(self, filename=None):
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        self.filename = filename
        self.file = None

    def start(self, sr=44100, nchannels=2):
        self.file = wave.open(self.filename, 'wb')
        self.file.setnchannels(nchannels)
        self.file.setsampwidth(2)  # 16-bit
        self.file.setframerate(sr)
        self.file.setnframes(0)

    def write(self, audio_data):
        # Convert float32 to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        self.file.writeframes(audio_int16.tobytes())

    def stop(self):
        self.file.close()