import whisper
from dotenv import load_dotenv
import os
load_dotenv()
from uuid import uuid4

class Transcriber:
    def __init__(self, model_name: str = "turbo"):
        """
        Initialize the Transcriber with a specified Whisper model.
        
        :param model_name: The name of the Whisper model to use (e.g., 'tiny', 'base', 'small', 'medium', 'large').
        """
        self.model = whisper.load_model(model_name)

    def get_transcription(self, audio_path: str) -> str:
        """
        Transcribe the audio file at the specified path using the Whisper model.
        
        :param audio_path: The path to the audio file to transcribe.
        :return: The transcription of the audio file.
        """
        result = self.model.transcribe(audio_path)
        # print(f"Transcription result: {result['text']}")
        return result['text']
    
    def save_audio_file(self, audio_file, file_type: str) -> str:
        """
        Save the audio file to a specified path.
        
        :param audio_file: The audio file to save.
        :param file_type: The type of the audio file (e.g., 'mp3', 'wav').
        :return: The path where the audio file is saved.
        """
        consultation_id = uuid4().hex
        audio_dir = os.getenv("AUDIO_DIR", "audio_files/")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        file_path = os.path.join(audio_dir, f"audio_{consultation_id}.{file_type}")
        try:
            audio_file.save(file_path)
            print(f"Audio file saved at: {file_path} ")
        except Exception as e:
            print(f"Failed to save audio file: {e}")
            raise e
        return file_path, consultation_id