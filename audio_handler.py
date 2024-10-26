import torch
from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
import sounddevice as sd
import numpy as np

# Initialize Whisper model
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, low_cpu_mem_usage=True)
processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    device=device,
)

def record_audio(duration=5, fs=16000):
    print("Recording started...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("Recording stopped.")
    return np.squeeze(audio)

def transcribe_audio(audio):
    # Convert to 16-bit PCM and resample if needed
    # Then pass the file or stream to the Whisper pipeline
    result = pipe(audio)
    print("Transcription:", result["text"])
    return result["text"]

# Start recording
audio_data = record_audio()  # Record a short clip
text = transcribe_audio(audio_data)  # Transcribe it

