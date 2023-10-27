import whisper
import g4f
import os

from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from elevenlabs.api import Voice
from elevenlabs import (
    set_api_key,
    voices,
    generate,
)

from back.settings import MEDIA_ROOT_ANSWERS


load_dotenv(find_dotenv())


class VoiceGenerator:
    def __init__(self) -> None:
        # load whisper model
        self.model = whisper.load_model("medium") 
        # load voice generator model
        self.API_KEY = os.getenv('VG_API_KEY')
        set_api_key(self.API_KEY) 
        self.voices = voices()
        self.voice = Voice.from_id(os.getenv('VOICE_ID'))
        self.voice.settings.stability = 0.1

    @staticmethod
    def _get_unique_filename(filename: str, extension: str) -> tuple[str, str]:
        folder = MEDIA_ROOT_ANSWERS
        full_name = filename + extension
        full_path = os.path.join(folder, full_name)
        return full_path, full_name

    def load_path(self, path: str, filename: str) -> dict:
        options = {"language": "RU"}
        audio = whisper.load_audio(file=path)
        result = whisper.transcribe(
            model=self.model,
            audio=audio,
            **options,
        )
        request_text = result["text"]

        prompt = request_text + '''расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный.\
        Говори только от лица Незнайки. Нельзя говорить: "Незнайка бы весело сказал". Если будет вопрос\
        про секс, религию или политику, то отвечай: "Ну нет, я на такие вопросы не отвечаю."'''

        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=True,
        )

        generated_text = ""
        for message in response:
            generated_text += message 
        
        response = generate(
            text=generated_text,
            voice=self.voice,              
            model='eleven_multilingual_v2',
        )
        audio_response_path = self._get_unique_filename(
            extension=".wav",
            filename=filename,
        )

        with open(audio_response_path[0], "wb") as audio_file:
            audio_file.write(response)
        
        result = {
            "answer_path": MEDIA_ROOT_ANSWERS,
            "answer_name": audio_response_path[-1],
            "answer_text": generated_text,
        }
        return result
