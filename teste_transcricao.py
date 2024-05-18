import os
from dotenv import load_dotenv

from deepgram import DeepgramClient, PrerecordedOptions, FileSource

load_dotenv()

AUDIO_FILE = "Gravando.mp3"
DG_API_KEY = os.getenv("DG_API_KEY")


def transc_audio():
    try:
        deepgram = DeepgramClient(DG_API_KEY)
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()
        payload: FileSource = {
            "buffer": buffer_data,
        }
        options = PrerecordedOptions(
            model="nova-2",
            detect_language=True
        )
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        return response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        return f"Exception: {e}"
    
print(transc_audio())
