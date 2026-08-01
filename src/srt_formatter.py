import datetime

def format_timestamp(seconds: float) -> str:
    """Converts seconds into SRT timestamp format: HH:MM:SS,mmm"""
    delta = datetime.timedelta(seconds=seconds)
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds_remaining = divmod(remainder, 60)
    milliseconds = int((seconds - total_seconds) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds_remaining:02d},{milliseconds:03d}"

def generate_srt(transcription_segments: list) -> str:
    """
    Generates SRT formatted string from Whisper segments.
    Expected format of segments: [{'start': 0.0, 'end': 2.5, 'text': 'Hello'}, ...]
    """
    srt_output = []
    for index, segment in enumerate(transcription_segments, start=1):
        start_str = format_timestamp(segment['start'])
        end_str = format_timestamp(segment['end'])
        text = segment['text'].strip()
        
        srt_entry = f"{index}\n{start_str} --> {end_str}\n{text}\n"
        srt_output.append(srt_entry)
        
    return "\n".join(srt_output)
