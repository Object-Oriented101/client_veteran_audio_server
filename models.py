from abc import ABC, abstractmethod
import numpy as np
import whisper

# Abstract base class for models
class BaseModel(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def transcribe(self, audio_data):
        pass

# Whisper model subclass
class WhisperModel(BaseModel):
    def __init__(self, model_name="base.en"):
        self.model = self.load_model(model_name)

    def load_model(self, model_name):
        return whisper.load_model(model_name)

    def transcribe(self, audio_data, use_fp16=False):
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        result = self.model.transcribe(audio_np, fp16=use_fp16)
        return result['text'].strip()
