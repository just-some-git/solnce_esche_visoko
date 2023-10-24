import whisper
from elevenlabs import set_api_key, voices, generate
from elevenlabs.api import Voice
import g4f
import os
from datetime import datetime

class VoiceGenerator:
    def __init__(self):
        # load whisper model
        self.model = whisper.load_model("medium") 
        # load voice generator model
        self.API_KEY = 'e8674ea3cacda897ad20e57e6786fa26'
        set_api_key(self.API_KEY) 
        self.voices = voices()
        self.voice = Voice.from_id('8AsiUYrhphlnBNuggBCK')
        self.voice.settings.stability = 0.1

    def _get_unique_filename(self, prefix, extension):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder = "answer"
        filename = f"{prefix}_{timestamp}.{extension}"
        full_path = os.path.join(folder, filename)

        return full_path

    def load_path(self, path):
        options = {"language": "RU"}
        audio = whisper.load_audio(path)
        result = whisper.transcribe(self.model, audio, **options)
        request_text = result["text"]

        prompt = request_text + 'расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный. \
        Говори только от лица Незнайки. Нельзя говорить: Незнайка бы весело сказал. Если будет вопрос\
        про секс, религию или политику,то отвечай: "Ну неет, я на такие вопросы не отвечаю"'

        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"user", "content":prompt}],
            stream=True,
        )
        generated_text = ""

        for message in response:
            generated_text += message 
        
        response = generate(
            text=generated_text,
            voice=self.voice,              
            model='eleven_multilingual_v2'
        )
        
        audio_response_path = self._get_unique_filename("audio_response", "wav")
        with open(audio_response_path, "wb") as audio_file:
            audio_file.write(response)
        
        result = {}
        result["path"] = audio_response_path
        result["answer"] = generated_text
        
        return result
         