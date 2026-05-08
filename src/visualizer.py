from scapy.all import IP, TCP, UDP, ICMP
from collections import deque
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class TerminalVisualizer:
    def __init__(self, max_packets=50):
        self.packet_log = deque(maxlen=max_packets)
        self.protocol_counts = {'TCP': 0, 'UDP': 0, 'ICMP': 0}
        self.status = "Idle"
        self.live = Live(self._build_layout(), refresh_per_second=1)

    def _build_layout(self):
        protocol_table = Table(title="Protocol Distribution")
        protocol_table.add_column("Protocol")
        protocol_table.add_column("Count")
        for proto, count in self.protocol_counts.items():
            protocol_table.add_row(proto, str(count))
        
        packet_table = Table(title="Recent Packets")
        packet_table.add_column("Time")
        packet_table.add_column("Source")
        packet_table.add_column("Destination")
        packet_table.add_column("Protocol")
        packet_table.add_column("Size")
        for packet in reversed(self.packet_log):
            packet_table.add_row(*packet)
        
        status_panel = Panel(Text(self.status, style="bold green"), title="Status")
        
        return Panel.Group(protocol_table, packet_table, status_panel)

    def update_packet(self, packet):
        if packet.haslayer(TCP):
            proto = 'TCP'
            self.protocol_counts['TCP'] += 1
        elif packet.haslayer(UDP):
            proto = 'UDP'
            self.protocol_counts['UDP'] += 1
        elif packet.haslayer(ICMP):
            proto = 'ICMP'
            self.protocol_counts['ICMP'] += 1
        else:
            proto = 'Other'
        
        src = packet[IP].src
        dst = packet[IP].dst
        size = packet.len
        self.packet_log.append((datetime.now().strftime("%H:%M:%S"), src, dst, proto, str(size)))
        
        self.live.update(self._build_layout())

    def start(self):
        self.live.start()

    def stop(self):
        self.live.stop()