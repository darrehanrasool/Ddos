"""Audio Alert System for DDoS-AI Platform.

Provides programmatic audio alerts, distinct beeping tones for threat levels
(Safe/Normal = Green chime, Caution/Rate-Limit = Yellow warning, Attack/DDoS = Red danger alarm,
Critical/Block = Siren), online sound downloader, and non-blocking system sound playback via macOS afplay.
"""

import math
import os
import struct
import subprocess
import threading
import time
import urllib.request
import wave
from pathlib import Path
from typing import Dict, Optional


class AudioSynthesizer:
    """Synthesizes clean, high-fidelity 16-bit PCM WAV alert sounds."""

    @staticmethod
    def generate_sine_wave(
        freq: float, duration: float, sample_rate: int = 44100, volume: float = 0.5
    ) -> list:
        """Generates a pure sine wave with smooth attack/decay envelope."""
        n_samples = int(sample_rate * duration)
        samples = []
        attack_len = int(sample_rate * min(0.02, duration * 0.1))
        decay_len = int(sample_rate * min(0.05, duration * 0.2))

        for i in range(n_samples):
            t = i / sample_rate
            # Compute envelope
            if i < attack_len:
                envelope = i / attack_len
            elif i > n_samples - decay_len:
                envelope = (n_samples - i) / decay_len
            else:
                envelope = 1.0

            raw = volume * envelope * math.sin(2.0 * math.pi * freq * t)
            samples.append(raw)
        return samples

    @staticmethod
    def generate_harmonic_chime(
        frequencies: list, duration: float, sample_rate: int = 44100, volume: float = 0.4
    ) -> list:
        """Generates a multi-frequency harmonious chime with exponential decay."""
        n_samples = int(sample_rate * duration)
        samples = []
        for i in range(n_samples):
            t = i / sample_rate
            # Exponential decay
            decay = math.exp(-3.5 * t / duration)
            sample_val = 0.0
            for f in frequencies:
                sample_val += math.sin(2.0 * math.pi * f * t)
            sample_val = (sample_val / len(frequencies)) * decay * volume
            samples.append(sample_val)
        return samples

    @staticmethod
    def generate_fm_siren(
        base_freq: float,
        mod_freq: float,
        mod_index: float,
        duration: float,
        sample_rate: int = 44100,
        volume: float = 0.6,
    ) -> list:
        """Generates an urgent frequency-modulated siren alarm."""
        n_samples = int(sample_rate * duration)
        samples = []
        for i in range(n_samples):
            t = i / sample_rate
            inst_freq = base_freq + mod_index * math.sin(2.0 * math.pi * mod_freq * t)
            sample_val = volume * math.sin(2.0 * math.pi * inst_freq * t)
            samples.append(sample_val)
        return samples

    @classmethod
    def write_wav(cls, filepath: Path, samples: list, sample_rate: int = 44100):
        """Writes floating point audio samples [-1.0, 1.0] to a 16-bit PCM mono WAV file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(filepath), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            frames = bytearray()
            for s in samples:
                # Clamp sample
                clamped = max(-1.0, min(1.0, s))
                int_sample = int(clamped * 32767.0)
                frames.extend(struct.pack("<h", int_sample))
            wav_file.writeframes(frames)


class AudioAlertManager:
    """Manages audio alerts, online sound downloads, and non-blocking sound playback."""

    ONLINE_SOUND_RESOURCES = {
        "safe_normal": "https://raw.githubusercontent.com/wesbos/JavaScript30/master/01%20-%20JavaScript%20Drum%20Kit/sounds/tink.wav",
        "warning_alert": "https://raw.githubusercontent.com/wesbos/JavaScript30/master/01%20-%20JavaScript%20Drum%20Kit/sounds/hihat.wav",
        "danger_ddos": "https://raw.githubusercontent.com/wesbos/JavaScript30/master/01%20-%20JavaScript%20Drum%20Kit/sounds/snare.wav",
        "critical_block": "https://raw.githubusercontent.com/wesbos/JavaScript30/master/01%20-%20JavaScript%20Drum%20Kit/sounds/boom.wav",
    }

    def __init__(self, sounds_dir: Optional[Path] = None, enable_audio: bool = True):
        if sounds_dir is None:
            self.sounds_dir = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "sounds"
        else:
            self.sounds_dir = Path(sounds_dir)

        self.sounds_dir.mkdir(parents=True, exist_ok=True)
        self.enable_audio = enable_audio
        self.last_played_time = 0.0
        self.cooldown_sec = 0.35  # Prevent audio clipping from rapid packet streams
        self.lock = threading.Lock()

        # Initialize audio files
        self.ensure_sound_files()

    def ensure_sound_files(self):
        """Generates studio-quality alert sound files if they do not exist."""
        sound_files = {
            "safe_normal.wav": self._create_safe_chime,
            "warning_alert.wav": self._create_warning_beep,
            "danger_ddos.wav": self._create_danger_alarm,
            "critical_block.wav": self._create_critical_siren,
        }

        for filename, generator_fn in sound_files.items():
            dest = self.sounds_dir / filename
            if not dest.exists():
                generator_fn(dest)

    def download_online_sounds(self, timeout: int = 4) -> Dict[str, bool]:
        """Attempts to download sound effects from online public audio repositories.
        
        Falls back automatically to local high-fidelity synthesized WAVs if offline.
        """
        results = {}
        for name, url in self.ONLINE_SOUND_RESOURCES.items():
            dest = self.sounds_dir / f"{name}_online.wav"
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "DDoS-AI-Security-Alert-Client/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    data = response.read()
                    if len(data) > 100:  # Valid audio payload
                        dest.write_bytes(data)
                        results[name] = True
                    else:
                        results[name] = False
            except Exception:
                # Offline or timeout, keep synthetic WAV
                results[name] = False
        return results

    def _create_safe_chime(self, dest: Path):
        """Safe Traffic (Green): Calming 3-note harmonic major chord (C5 + E5 + G5)."""
        samples = AudioSynthesizer.generate_harmonic_chime(
            frequencies=[523.25, 659.25, 783.99],
            duration=0.45,
            volume=0.35,
        )
        AudioSynthesizer.write_wav(dest, samples)

    def _create_warning_beep(self, dest: Path):
        """Warning / Anomaly (Yellow): Double amber caution beep (660 Hz)."""
        beep1 = AudioSynthesizer.generate_sine_wave(660.0, 0.08, volume=0.45)
        silence = [0.0] * int(44100 * 0.04)
        beep2 = AudioSynthesizer.generate_sine_wave(660.0, 0.08, volume=0.45)
        AudioSynthesizer.write_wav(dest, beep1 + silence + beep2)

    def _create_danger_alarm(self, dest: Path):
        """Danger / DDoS Attack (Red): Urgent oscillating dual-frequency warble siren."""
        samples = AudioSynthesizer.generate_fm_siren(
            base_freq=950.0,
            mod_freq=9.0,
            mod_index=280.0,
            duration=0.55,
            volume=0.60,
        )
        AudioSynthesizer.write_wav(dest, samples)

    def _create_critical_siren(self, dest: Path):
        """Critical Threat / Defense Block (Deep Red): Rapid triple staccato defensive alarm."""
        samples = []
        for _ in range(3):
            samples.extend(AudioSynthesizer.generate_sine_wave(1320.0, 0.06, volume=0.65))
            samples.extend([0.0] * int(44100 * 0.03))
        # Deep confirmation tone
        samples.extend(AudioSynthesizer.generate_sine_wave(220.0, 0.15, volume=0.55))
        AudioSynthesizer.write_wav(dest, samples)

    def get_sound_path(self, alert_type: str) -> Optional[Path]:
        """Resolves the sound file path for a given alert type."""
        mapping = {
            "safe": "safe_normal.wav",
            "normal": "safe_normal.wav",
            "warning": "warning_alert.wav",
            "caution": "warning_alert.wav",
            "danger": "danger_ddos.wav",
            "attack": "danger_ddos.wav",
            "ddos": "danger_ddos.wav",
            "critical": "critical_block.wav",
            "block": "critical_block.wav",
        }
        filename = mapping.get(alert_type.lower(), "safe_normal.wav")
        # Check if online downloaded version exists
        online_name = filename.replace(".wav", "_online.wav")
        if (self.sounds_dir / online_name).exists():
            return self.sounds_dir / online_name
        
        path = self.sounds_dir / filename
        return path if path.exists() else None

    def play_sound(self, alert_type: str, force: bool = False):
        """Plays the designated alert sound asynchronously on macOS via afplay."""
        if not self.enable_audio:
            return

        now = time.time()
        with self.lock:
            if not force and (now - self.last_played_time < self.cooldown_sec):
                return
            self.last_played_time = now

        sound_path = self.get_sound_path(alert_type)
        if not sound_path:
            return

        # Run non-blocking in a background thread to prevent blocking pipeline execution
        def _play_worker(path_str):
            try:
                # Check for macOS afplay
                if os.path.exists("/usr/bin/afplay"):
                    subprocess.run(
                        ["/usr/bin/afplay", path_str],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                else:
                    # Linux fallback (aplay or paplay)
                    for player in ["paplay", "aplay"]:
                        if subprocess.run(["which", player], stdout=subprocess.DEVNULL).returncode == 0:
                            subprocess.run([player, path_str], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            break
            except Exception:
                pass

        thread = threading.Thread(target=_play_worker, args=(str(sound_path),), daemon=True)
        thread.start()


# Global singleton helper
_global_audio_manager: Optional[AudioAlertManager] = None


def get_audio_manager() -> AudioAlertManager:
    """Returns the global AudioAlertManager instance."""
    global _global_audio_manager
    if _global_audio_manager is None:
        _global_audio_manager = AudioAlertManager()
    return _global_audio_manager


def play_threat_sound(threat_level: str):
    """Convenience helper to play sound for 'safe', 'warning', 'danger', or 'critical'."""
    get_audio_manager().play_sound(threat_level)
