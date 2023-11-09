import g4f
import os

from datetime import datetime
from elevenlabs.api import Voice
from dotenv import load_dotenv, find_dotenv
from elevenlabs import (
    set_api_key,
    voices,
    generate,
)

from back.settings import MEDIA_ROOT_ANSWERS


load_dotenv(find_dotenv())


class VoiceGeneratorFromText:

    def __init__(self) -> None:
        self.API_KEY = os.getenv('VG_API_KEY')
        set_api_key(self.API_KEY)
        self.voices = voices()
        self.voice = Voice.from_id(os.getenv('VOICE_ID'))
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

    @staticmethod
    def _get_unique_filename(prefix: str, extension: str) -> tuple[str, str]:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        full_path = os.path.join(MEDIA_ROOT_ANSWERS, filename)

        return full_path, filename

    def _use_GPT(self, prompt: str) -> str:
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

        text = ""
        for message in response:
            text += message

        return text

    def generate_answer(self, text: str) -> dict[str, str]:
        # инициализация словаря - результата запроса
        # фиксация времени начала выполнения кода
        result = {"timestamp": "start " + datetime.now().strftime("%M:%S")}

        # переопределяем входную переменную в локальную, которая у нас есть в изначальном классе
        # в первом варианте сюда присваивается текстовое значение результата считывания голоса whisper
        request_text = text

        # создаем промпты для определия темы запроса и эмоционального окраса текста запроса, основной
        # промпт берем из глобальной переменной
        prompt_topic = f'{request_text} определи тему вопроса из предложенных тем: {self.topics} \
        Представь, что ты можешь точно определить тему и выведи только одно единственное ее название'
        prompt_emo = request_text + ' - определи эмоцию вопроса из вариантов: веселая, нейтральная, грустная, озабоченная. \
            ответ должен быть одним словом из предложенных эмоций'
        prompt_request = request_text + self.prompt_request_template

        # обращаемся к GPT-3.5 через api g4f
        topic_text = self._use_GPT(prompt_topic)
        result["timestamp"] += " text topic " + datetime.now().strftime("%M:%S")
        emo_text = self._use_GPT(prompt_emo)
        result["timestamp"] += " text emo " + datetime.now().strftime("%M:%S")
        generated_text = self._use_GPT(prompt_request)
        result["timestamp"] += " text generated " + datetime.now().strftime("%M:%S")

        # синтезируем речь
        audio_response = generate(
            text=generated_text,
            voice=self.voice,
            model='eleven_multilingual_v2',
        )
        audio_response_path = self._get_unique_filename(
            prefix="audio_response",
            extension="wav",
        )

        with open(
                file=audio_response_path[0],
                mode="wb",
        ) as audio_file:
            audio_file.write(audio_response)

        result["timestamp"] += " syntez complete " + datetime.now().strftime("%M:%S")

        result["filename"] = audio_response_path[-1]
        result["path"] = audio_response_path[0]
        result["topic"] = topic_text
        result["emotion"] = emo_text
        result["answer"] = generated_text

        return result
