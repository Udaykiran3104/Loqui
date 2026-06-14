import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile, os

SAMPLE_RATE = 16000   # Whisper expects 16kHz

class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.recording = False

    def start(self):
        self.frames = []
        self.recording = True
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32',
            callback=self._callback
        )
        self._stream.start()
        print("🎙️  Recording...")

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def stop(self) -> str:
        """Stop recording, save to temp WAV, return file path."""
        self.recording = False
        self._stream.stop()
        self._stream.close()

        audio = np.concatenate(self.frames, axis=0)
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        write(tmp.name, SAMPLE_RATE, audio)
        print(f"⏹️  Saved: {tmp.name}")
        return tmp.name
