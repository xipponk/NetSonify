# NetSonify

A network packet sonification tool that converts network traffic into sound using scapy, numpy, and sounddevice.

## Installation

```bash
mkdir -p src config tests recordings
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py -i eth0
```

### Options
- `-i, --iface`: Network interface to sniff on (default: `eth0`)
- `-c, --config`: Path to config file (default: `config/default.yaml`)
- `-v, --verbose`: Enable verbose output
- `--record`: Record audio to file
- `--no-vis`: Disable terminal visualizer

## Configuration

The default configuration is in `config/default.yaml`:

```yaml
iface: eth0
sample_rate: 44100
verbose: false
record: false
no_vis: false
```

## Verification

```bash
py_compile src/*.py
pytest tests/ -v
```

## Dependencies

- scapy>=2.5.0
- numpy>=1.26.0
- sounddevice>=0.4.6
- PyYAML>=6.0
- rich>=13.7.0