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
        self.topics = 'Погода, Политика, Спорт,\
        Рецепты и кулинария, здоровье и медицина, Фитнес и упражнения, Путешествия и туризм, \
        Образование и учеба, Фильмы и киноиндустрия, Музыка и концерты, Технологии и гаджеты, \
        Социальные сети (Facebook, Instagram, Twitter), Мода и стиль, Игры (компьютерные и мобильные),\
        Книги и литература, Финансы и инвестиции, Автомобили и автопром, Компьютерное программирование, \
        Искусство и художественная культура, Дизайн и графика, Психология и отношения, Домашние животные, \
        События и праздники, Еда и рестораны, Интерьер и декор, Дети и семья, Спортивные мероприятия, \
        Космос и астрономия, Экология и охрана окружающей среды, Городская жизнь, Путешествия и отпуск, \
        Свадьбы и мероприятия, Виртуальная реальность и дополненная реальность, Забавы и развлечения, \
        Веганство и здоровое питание, Саморазвитие и самопомощь, хобби и ремесла,\
        Психическое здоровье и благополучие, Астрология и гороскопы, Наука и исследования, \
        Бизнес и предпринимательство, Туризм и путешествия, криптовалюты и биткоин,\
        Социокультурные движения и активизм, Мотивация и успех, гаджеты и технические новинки,\
        Фотография и видеосъемка, История и культурное наследие, Языки и обучение иностранным языкам, Природа и путешествия,\
        Секс, Религия.'
        # Определение переменной шаблона для промпта
        self.prompt_request_template = 'расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный, не более 50 символов. \
        Говори только от лица Незнайки. Если будет вопрос про секс, религию или политику,то отвечай: "Ну неет, я на такие вопросы не отвечаю)" \
        Иначе отвечай шуточно и весело, как бы сказал Незнайка.'

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
        result = {}
        result["timestamp"] = "start " + datetime.now().strftime("%M:%S")
        options = {"language": "RU"}
        audio = whisper.load_audio(path)
        request = whisper.transcribe(self.model, audio, **options)
        request_text = request["text"]

        prompt_topic = f'давай поиграем в игру: ты отвечаешь только словами из следующего списка: {self.topics} \
        ответь подбери наиболее подходящий вариант из твоего списка слов: ' + request_text
        prompt_emo = request_text + ' - определи эмоцию вопроса из вариантов: веселая, нейтральная, грустная, озабоченная. \
            ответ должен быть одним словом из предложенных эмоций'
        prompt_request = request_text + self.prompt_request_template
        
        topic_text = self._use_GPT(prompt_topic)
        result["timestamp"] += " text topic " + datetime.now().strftime("%M:%S")
        emo_text = self._use_GPT(prompt_emo)
        result["timestamp"] += " text emo " + datetime.now().strftime("%M:%S")
        generated_text = self._use_GPT(prompt_request)
        result["timestamp"] += " text generated " + datetime.now().strftime("%M:%S")
        
        audio_response = generate(
            text=generated_text,
            voice=self.voice,              
            model='eleven_multilingual_v2'
        )
        
        audio_response_path = self._get_unique_filename("audio_response", "wav")
        with open(audio_response_path, "wb") as audio_file:
            audio_file.write(audio_response)
        result["timestamp"] += " syntez complete " + datetime.now().strftime("%M:%S")
        
        result["request"] = request_text
        result["topic"] = topic_text
        result["emotion"] = emo_text
        result["path"] = audio_response_path
        result["answer"] = generated_text
        
        return result