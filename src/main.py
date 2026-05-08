print("NetSonify v1.0 - Network Audio Sonification Tool")
print("Starting up...")

import argparse
import yaml
from collections import deque
import threading
import time
import sys
import os
import datetime

recorder = None

try:
    parser = argparse.ArgumentParser(description='NetSonify: Network Packet Sonification')
    parser.add_argument('-i', '--iface', required=True, help='Network interface to sniff on')
    parser.add_argument('-c', '--config', default='config/default.yaml', help='Path to config file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--record', action='store_true', help='Record audio to file')
    parser.add_argument('--no-vis', action='store_true', help='Disable visualizer')
    args = parser.parse_args()

    if args.record:
        os.makedirs('recordings', exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/capture_{timestamp}.wav"
        print(f"Recording to: {filename}")
        from .recorder import WavRecorder
        recorder = WavRecorder(filename=filename)
        recorder.start(sr=44100, nchannels=1)

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
except Exception as e:
    print(f"Error loading config: {e}")
    sys.exit(1)

packet_queue = deque(maxlen=1000)
stop_event = threading.Event()

from .sniffer import PacketSniffer
from .player import AudioPlayer

sniffer = PacketSniffer(iface=args.iface, queue=packet_queue)
player = AudioPlayer(packet_deque=packet_queue, config=config, record=args.record, no_vis=args.no_vis, recorder=recorder)

sniffer.start()
player.start(daemon=True)

try:
    while not stop_event.is_set():
        time.sleep(1)
except KeyboardInterrupt:
    stop_event.set()
    print("Stopping...")
    if recorder is not None:
        recorder.stop()
    sys.exit(0)
except Exception as e:
    print(f"Critical error: {e}")
    if recorder is not None:
        recorder.stop()
    sys.exit(1)
