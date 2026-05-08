from collections import deque
from scapy.all import AsyncSniffer, IP

class PacketSniffer:
    def __init__(self, iface=None, queue=None):
        self.deque = queue if queue is not None else deque()
        self.sniffer = AsyncSniffer(iface=iface, filter="ip", prn=self._callback)

    def _callback(self, packet):
        if packet.haslayer(IP):
            print(f"Packet captured: {packet[IP].src} -> {packet[IP].dst}", flush=True)
            self.deque.append(packet)
            print("Packet added to queue", flush=True)

    def start(self):
        self.sniffer.start()

    def stop(self):
        self.sniffer.stop()
