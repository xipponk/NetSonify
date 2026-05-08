from collections import deque
import threading
import time
import sounddevice as sd
from .mapper import PacketMapper
from .synth import generate_note

class AudioPlayer:
    def __init__(self, packet_deque, sr=44100, config=None, record=False, no_vis=False, recorder=None):
        self.packet_deque = packet_deque
        self.sr = sr
        self.config = config
        self.record = record
        self.no_vis = no_vis
        self.recorder = recorder
        self.mapper = PacketMapper()
        self._thread = None

    def play(self):
        while True:
            if self.packet_deque:
                packet = self.packet_deque.popleft()
                freq, pan = self.mapper.map_packet(packet)
                note = generate_note(freq, duration=0.1, pan=pan, amplitude=0.5, sr=self.sr)
                try:
                    sd.play(note, samplerate=self.sr)
                    sd.wait()
                except Exception:
                    pass  # ไม่มี audio device — ข้ามไป
                if self.recorder is not None:
                    self.recorder.write(note)
            else:
                time.sleep(0.01)

    def start(self, daemon=False):
        self._thread = threading.Thread(target=self.play, daemon=daemon)
        self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._thread.join(timeout=1)
