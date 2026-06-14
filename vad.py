import torch, numpy as np
from scipy.io.wavfile import read as wav_read, write as wav_write
import tempfile

# Load silero-vad model (downloads ~2MB once, cached after)
model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)
(get_speech_timestamps, _, _, *_) = utils

def trim_silence(wav_path: str) -> str:
    """Return path to silence-trimmed WAV."""
    sr, audio_np = wav_read(wav_path)
    if audio_np.dtype != np.float32:
        audio_np = audio_np.astype(np.float32) / np.iinfo(audio_np.dtype).max
    audio = torch.from_numpy(audio_np)

    timestamps = get_speech_timestamps(audio, model, sampling_rate=16000)

    if not timestamps:
        return wav_path   # no speech found, return as-is

    # Merge all speech segments
    speech = torch.cat([
        audio[t['start']:t['end']] for t in timestamps
    ])

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav_write(tmp.name, 16000, speech.numpy())
    return tmp.name
