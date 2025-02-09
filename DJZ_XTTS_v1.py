#!/usr/bin/env python
import os
import torch
import numpy as np
from TTS.api import TTS

class DJZ_XTTS_v1:
    def __init__(self):
        self.type = "DJZXTTS_v1"
        self.output_type = "AUDIO"
        self.output_dims = 1
        self.compatible_decorators = []
        self.required_extensions = []
        self.category = "Text-to-Speech"
        self.name = "DJZ XTTS Processor"
        self.description = "Converts input text to speech using XTTS with language selection."

    def initialize_tts(self):
        # Determine the device: CUDA if available, otherwise CPU.
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Initialize the XTTS model.
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        return tts

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello, world!"}),
                "language": (["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn"], {"default": "en"})
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "synthesize"

    def synthesize(self, text, language):
        print(f"Synthesizing speech for text: {text} with language: {language}")
        try:
            tts = self.initialize_tts()
            # Use default speaker if available.
            if hasattr(tts, "speakers") and tts.speakers:
                default_speaker = tts.speakers[0]
                wav = tts.tts(text=text, language=language, speaker=default_speaker)
            else:
                wav = tts.tts(text=text, language=language)
            wav = np.array(wav, dtype=np.float32)
            sample_rate = 22050
        except Exception as e:
            raise ValueError(f"Error generating speech: {str(e)}")

        # Convert wav to torch tensor and adjust dimensions.
        if isinstance(wav, list):
            wav = np.array(wav)
        if wav.ndim == 1:
            wav = np.expand_dims(np.expand_dims(wav, 0), 0)
        elif wav.ndim == 2:
            wav = np.expand_dims(wav, 0)
        elif wav.ndim == 3:
            pass
        else:
            raise ValueError("Unexpected shape for generated audio samples.")

        try:
            audio_tensor = torch.from_numpy(wav).float()
        except Exception as e:
            raise ValueError(f"Failed to convert samples to tensor: {str(e)}")

        if audio_tensor.dim() == 2:
            audio_tensor = audio_tensor.unsqueeze(1)
        elif audio_tensor.dim() == 3 and audio_tensor.shape[1] > audio_tensor.shape[2]:
            audio_tensor = audio_tensor.transpose(1, 2)

        result = {
            "waveform": audio_tensor.contiguous().detach(),
            "sample_rate": sample_rate,
            "path": None
        }
        print("DJZ-XTTS synthesis complete.")
        return (result,)

NODE_CLASS_MAPPINGS = {
    "DJZ_XTTS_v1": DJZ_XTTS_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZ_XTTS_v1": "DJZ XTTS v1"
}
