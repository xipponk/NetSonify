from collections import deque
import sounddevice as sd
from .mapper import PacketMapper
from .synth import generate_note

class AudioPlayer:
    def __init__(self, packet_deque, sr=44100):
        self.packet_deque = packet_deque
        self.sr = sr
        self.mapper = PacketMapper()

    def play(self):
        while self.packet_deque:
            packet = self.packet_deque.popleft()
            freq, pan = self.mapper.map_packet(packet)
            note = generate_note(freq, duration=0.1, pan=pan, amplitude=0.5, sr=self.sr)
            sd.play(note, samplerate=self.sr)
            sd.wait()