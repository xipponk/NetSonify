import numpy as np

def generate_note(freq, duration, pan, amplitude, sr):
    # Generate time array
    t = np.linspace(0, duration, int(duration * sr), endpoint=False)
    
    # Generate sine wave
    sine = np.sin(2 * np.pi * freq * t)
    
    # ADSR envelope parameters (default)
    attack_time = 0.01
    decay_time = 0.05
    sustain_level = 0.8
    release_time = 0.1
    
    # Calculate envelope
    envelope = np.zeros(len(t))
    total_samples = len(t)
    
    # Attack
    attack_samples = int(attack_time * sr)
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    decay_samples = int(decay_time * sr)
    decay_start = attack_samples
    decay_end = decay_start + decay_samples
    if decay_end <= total_samples:
        envelope[decay_start:decay_end] = np.linspace(1, sustain_level, decay_samples)
    else:
        # Handle if decay goes beyond total samples
        envelope[decay_start:] = np.linspace(1, sustain_level, total_samples - decay_start)
    
    # Sustain (if any)
    sustain_start = decay_end
    sustain_end = total_samples - int(release_time * sr)
    if sustain_start < sustain_end:
        envelope[sustain_start:sustain_end] = sustain_level
    
    # Release
    release_start = total_samples - int(release_time * sr)
    if release_start < total_samples:
        envelope[release_start:] = np.linspace(sustain_level, 0, total_samples - release_start)
    
    # Apply envelope and amplitude
    note = sine * envelope * amplitude
    
    # Stereo panning
    left = note * (1 - pan) / 2
    right = note * (1 + pan) / 2
    
    # Combine into stereo array
    stereo = np.column_stack((left, right)).astype(np.float32)
    
    return stereo