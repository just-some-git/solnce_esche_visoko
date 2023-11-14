from elevenlabs import set_api_key, voices, generate
from elevenlabs.api import Voice
import g4f
import os
from datetime import datetime

class VoiceGenerator:
    def __init__(self):
        self.API_KEY = 'e8674ea3cacda897ad20e57e6786fa26'
        set_api_key(self.API_KEY) 
        self.voices = voices()
        self.voice = Voice.from_id('8AsiUYrhphlnBNuggBCK')
        self.voice.settings.stability = 0.1
        # список тем лучше предоставить в строковом формате, чтобы избежать лишний код по переводу списка в строку
        self.topics = 'Погода, Политика, Спорт, \
        Рецепты и кулинария, здоровье и медицина, Фитнес и упражнения, Путешествия и туризм, \
        Образование и учеба, Фильмы и киноиндустрия, Музыка и концерты, Технологии и гаджеты, \
        Социальные сети, Мода и стиль, Игры (компьютерные и мобильные), \
        Книги и литература, Финансы и инвестиции, Автомобили и автопром, Компьютерное программирование, \
        Искусство и художественная культура, Дизайн и графика, Психология и отношения, Домашние животные, \
        События и праздники, Еда и рестораны, Интерьер и декор, Дети и семья, Спортивные мероприятия, \
        Космос и астрономия, Экология и охрана окружающей среды, Городская жизнь, Путешествия и отпуск, \
        Свадьбы и мероприятия, Виртуальная реальность и дополненная реальность, Забавы и развлечения, \
        Веганство и здоровое питание, Саморазвитие и самопомощь, Хобби и ремесла, \
        Благополучие, Астрология и гороскопы, Наука и исследования, \
        Бизнес и предпринимательство, Туризм и путешествия, Криптовалюты и биткоин, \
        Социокультурные движения и активизм, Мотивация и успех, \
        Фотография и видеосъемка, История и культурное наследие, Иностранные языки, Природа и путешествия,\
        Секс, Религия, Противоправные действия, Наркотики, Война и боевые действия'
        self.banned_topics = 'Политика, Секс, Наркотики, Противоправные действия, Религия, Иностранные языки, \
        Война и боевые действия'
        self.emos = 'Веселая, Нейтральная, Грустная, Озабоченная, Дружественная, Формальная, Негативная, Оскорбительная'
        self.banned_emos = 'Негативная, Оскорбительная'
        self.prompt_topic_template = '. Представь, что ты можешь точно определить тему и \
        выведи только одно единственное ее название из предложенных тем: '
        self.prompt_emo_template = '. Представь, что ты можешь точно определить эмоцию и \
        выведи только одно единственное ее название из предложенных эмоций: '
        # Определение переменной шаблона для промпта
        self.prompt_request_template = '. Расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный, не более 50 символов. \
        Говори только от лица Незнайки, отвечай шуточно и весело, как бы сказал Незнайка.'

    def _get_unique_filename(self, prefix, extension):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder = "answer"
        # проверяем наличие папки аnswer, если она отсутствует, то создаем новую
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filename = f"{prefix}_{timestamp}.{extension}"
        full_path = os.path.join(folder, filename)

        return full_path
    
    def _use_GPT(self, prompt, counter=0):
        if counter >= 10:
            return "ой"
        
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"user", "content":prompt}],
            stream=True,
        )
        
        text = ""
        for message in response:
            text += message
            
        if "日" in text:
            text = self._use_GPT(prompt, counter + 1)        
            
        return text
    
    def _check_text(self, text, given_list):
        for given in given_list:
            if given.lower() in text.lower():
                return given
        return "Undefined"
    
    def _get_topic(self, request_text):
        prompt_topic = request_text + self.prompt_topic_template + self.topics
        generated_topic = self._use_GPT(prompt_topic)
        topics = self.topics.split(', ')
        topic_text = self._check_text(generated_topic, topics)
        
        return generated_topic, topic_text
        
    def _get_emo(self, request_text):
        prompt_emo = request_text + self.prompt_emo_template + self.emos
        generated_emo = self._use_GPT(prompt_emo)
        emos = self.emos.split(', ')
        emo_text = self._check_text(generated_emo, emos)
        
        return generated_emo, emo_text
    
    def _get_answer(self, request_text):
        prompt_request = request_text + self.prompt_request_template
        generated_text = self._use_GPT(prompt_request)
        
        return generated_text
        
    def _check_answer(self, generated_answer, topic_text, emo_text):
        if topic_text in self.banned_topics:
            return "Я на такие вопросы не отвечаю!"
        if emo_text in self.banned_emos:
            return "Ах ты грубиян!"
        return generated_answer        

    def _use_voice_syntesis(self, text):
        audio_response = generate(
            text=text,
            voice=self.voice,              
            model='eleven_multilingual_v2'
        )
        
        path = self._get_unique_filename("audio_response", "wav")
        with open(path, "wb") as audio_file:
            audio_file.write(audio_response)
        
        return path
    
    def generate_answer(self, request_text: str):
        result = {}
        result["request"] = request_text
        # фиксация времени начала выполнения кода
        result["timestamp"] = "start " + datetime.now().strftime("%M:%S")
        
        generated_topic, topic_text = self._get_topic(request_text=request_text)
        result["timestamp"] += " text topic " + datetime.now().strftime("%M:%S")
        generated_emo, emo_text = self._get_emo(request_text=request_text)
        result["timestamp"] += " text emo " + datetime.now().strftime("%M:%S")
        generated_answer = self._get_answer(request_text=request_text)
        result["timestamp"] += " text generated " + datetime.now().strftime("%M:%S")
        answer_text = self._check_answer(generated_answer, topic_text, emo_text)
        
        # синтезируем речь 
        result["path"] = self._use_voice_syntesis(generated_answer)
        result["timestamp"] += " syntez complete " + datetime.now().strftime("%M:%S")
        
        result ["generated_topic"], result["topic"] = generated_topic, topic_text
        result ["generated_emo"], result["emo"] = generated_emo, emo_text
        result ["generated_answer"], result["answer_text"] = generated_answer, answer_text
        
        return result