import argparse
from src.sniffer import PacketSniffer
from src.player import AudioPlayer


def main():
    parser = argparse.ArgumentParser(description='NetSonify - Network Packet Sonification')
    parser.add_argument('-i', '--iface', type=str, default='eth0', help='Network interface to sniff on')
    parser.add_argument('-c', '--config', type=str, default='config/default.yaml', help='Path to config file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--record', action='store_true', help='Record audio to file')
    parser.add_argument('--no-vis', action='store_true', help='Disable terminal visualizer')
    
    args = parser.parse_args()
    
    sniffer = PacketSniffer(iface=args.iface)
    sniffer.start()
    
    player = AudioPlayer(sniffer.deque)
    player.play()

if __name__ == '__main__':
    main()