from faster_whisper import WhisperModel
import yaml, os

class Transcriber:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)["model"]

        # Model downloads once to ~/.cache/huggingface/
        # After that — fully offline, zero network calls
        self.model = WhisperModel(
            cfg["size"],
            device=cfg.get("device", "cpu"),
            compute_type="int8"   # int8 = 2× faster on CPU, tiny quality loss
        )
        self.language = cfg.get("language", None)
        print(f"✅ Whisper '{cfg['size']}' loaded on {cfg.get('device','cpu')}")

    def transcribe(self, wav_path: str) -> str:
        segments, _ = self.model.transcribe(
            wav_path,
            language=self.language,
            beam_size=1,           # Reduced from 5 to 1 (Greedy decoding) for MUCH faster response times
            vad_filter=True,       # built-in basic VAD as backup
            vad_parameters=dict(min_silence_duration_ms=500),
            initial_prompt="Use correct punctuation. Do not use filler words like um, hm, hmm, mmm, uh, ah. Write clean text."
        )
        return " ".join(seg.text.strip() for seg in segments)
