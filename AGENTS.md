# NetSonify — Agent Instructions

## Stack
- Python 3.11, scapy, numpy, sounddevice, PyYAML, rich
- Structure: src/ config/ tests/ recordings/

## TASK 1: Create structure
mkdir -p src config tests recordings
touch src/__init__.py tests/__init__.py

## TASK 2: requirements.txt
scapy>=2.5.0
numpy>=1.26.0
sounddevice>=0.4.6
PyYAML>=6.0
rich>=13.7.0

## TASK 3: Setup venv
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

## TASK 4: Write src/sniffer.py
PacketSniffer class — AsyncSniffer, callback pushes to deque, IP layer only

## TASK 5: Write src/mapper.py  
PacketMapper class — TCP→220Hz, UDP→440Hz, ICMP→880Hz, size→pitch, port→offset, IP→pan

## TASK 6: Write src/synth.py
generate_note(freq, duration, pan, amplitude, sr) → stereo float32 ndarray, ADSR envelope

## TASK 7: Write src/player.py
AudioPlayer class — deque consumer, sounddevice.play, optional WavRecorder + Visualizer

## TASK 8: Write src/recorder.py
WavRecorder class — stdlib wave module, float32→int16, strftime filename

## TASK 9: Write src/visualizer.py
TerminalVisualizer class — rich Live, protocol bars, packet log table, status bar

## TASK 10: Write src/main.py
argparse CLI: -i iface, -c config, -v verbose, --record, --no-vis

## TASK 11: Write config/default.yaml and README.md

## TASK 12: Run verification
py_compile all src/*.py && pytest tests/ -v

Complete tasks sequentially. Write one file at a time.