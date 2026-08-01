import tempfile
import os
from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self, model_size: str = "base", device: str = "cpu", compute_type: str = "int8"):
        """
        Initializes the Faster-Whisper Model.
        """
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, file_bytes, file_extension: str):
        """
        Transcribes audio/video file bytes and returns structured segments.
        """
        # Temporary file Creation
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        try:
            segments, info = self.model.transcribe(temp_path, beam_size=5)
            
            result_segments = []
            for segment in segments:
                result_segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                })
                
            return result_segments
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
