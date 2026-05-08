from scapy.all import IP, TCP, UDP, ICMP

class PacketMapper:
    def map_packet(self, packet):
        if packet.haslayer(TCP):
            base_freq = 220
            port = packet[TCP].sport
        elif packet.haslayer(UDP):
            base_freq = 440
            port = packet[UDP].sport
        elif packet.haslayer(ICMP):
            base_freq = 880
            port = 0
        else:
            base_freq = 0
            port = 0

        size = packet.len
        freq = base_freq + (size * 0.1) + (port * 0.01)
        
        ip_src = packet[IP].src
        ip_last_octet = int(ip_src.split('.')[-1])
        pan = 1.0 if ip_last_octet % 2 == 1 else -1.0

        return freq, pan
