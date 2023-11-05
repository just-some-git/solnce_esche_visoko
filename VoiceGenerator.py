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
        # список тем лучше предоставить в строковом формате, чтобы избежать лишний код по переводу списка в строку
        self.topics = 'политика, праздник, природа, литературное произведение, спорт, внутренняя ситуация в россии, война, None'
        # Определение переменной шаблона для промпта
        self.prompt_request_template = 'расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный. \
        Говори только от лица Незнайки. Нельзя говорить: Незнайка бы весело сказал. Если будет вопрос\
        про секс, религию или политику,то отвечай: "Ну неет, я на такие вопросы не отвечаю"'

    def _get_unique_filename(self, prefix, extension):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder = "answer"
        # проверяем наличие папки аnswer, если она отсутствует, то создаем новую
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = f"{prefix}_{timestamp}.{extension}"
        full_path = os.path.join(folder, filename)

        return full_path
    
    def _use_GPT(self, prompt):
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"user", "content":prompt}],
            stream=True,
        )
        
        text = ""
        for message in response:
            text += message
            
        return text

    def load_path(self, path):
        options = {"language": "RU"}
        audio = whisper.load_audio(path)
        result = whisper.transcribe(self.model, audio, **options)
        request_text = result["text"]

        prompt_topic = f'давай поиграем в игру: ты отвечаешь только словами из следующего списка: {self.topics} \
        ответь подбери наиболее подходящий вариант из твоего списка слов: ' + request_text
        prompt_emo = request_text + ' - определи эмоцию вопроса из вариантов: веселая, нейтральная, грустная, озабоченная. \
            ответ должен быть одним словом из предложенных эмоций'
        prompt_request = request_text + self.prompt_request_template
        
        topic_text = self._use_GPT(prompt_topic)
        emo_text = self._use_GPT(prompt_emo)
        generated_text = self._use_GPT(prompt_request)
        
        audio_response = generate(
            text=generated_text,
            voice=self.voice,              
            model='eleven_multilingual_v2'
        )
        
        audio_response_path = self._get_unique_filename("audio_response", "wav")
        with open(audio_response_path, "wb") as audio_file:
            audio_file.write(audio_response)
        
        result = {}
        result["request"] = request_text
        result["topic"] = topic_text
        result["emotion"] = emo_text
        result["path"] = audio_response_path
        result["answer"] = generated_text
        
        return result