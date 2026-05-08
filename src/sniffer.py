from collections import deque
from scapy.all import AsyncSniffer, IP

class PacketSniffer:
    def __init__(self, iface=None):
        self.deque = deque()
        self.sniffer = AsyncSniffer(iface=iface, filter="ip", prn=self._callback)

    def _callback(self, packet):
        if packet.haslayer(IP):
            self.deque.append(packet)

    def start(self):
        self.sniffer.start()

    def stop(self):
        self.sniffer.stop()