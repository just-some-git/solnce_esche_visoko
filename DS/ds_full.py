#!/usr/bin/env python
# coding: utf-8

# ## Установка библиотек

# In[66]:


# pip install -U openai-whisper


# In[67]:


# pip install g4f


# In[68]:


# pip install ffmpeg


# In[69]:


# pip install elevenlabs


# In[70]:


import whisper


# In[71]:


model = whisper.load_model("medium") # загружаем модель ДО НАЧАЛА ВСЕГО ПРОЦЕССА, установка 3 мин 20 с


# In[72]:


from elevenlabs import set_api_key, voices, generate
from elevenlabs.api import Voice, Models


# In[73]:


import g4f


# ### Распознавание audio в текст

# str_path  - это путь к аудиофайлу любого формата

# In[74]:


# загрузите аудиофайл, здесь необходимо указать путь к вашему файлу!!!
str_path = 'Голос 115.m4a'

audio = whisper.load_audio(str_path)

options = {
    "language": "RU", # поставьте необходимый язык
}
result = whisper.transcribe(model, audio, **options)
text = result["text"]
print(text)


# ### Ответ на вопрос модели gpt

# In[75]:


# text = 'сколько планет в солнечной системе'
prompt = text + 'расскажи как бы объяснил Незнайка. Ответ должен быть короткий и шуточный. \
Говори только от лица Незнайки. Нельзя говорить: Незнайка бы весело сказал. Если будет вопрос\
про секс, религию или политику,то отвечай: "Ну неет, я на такие вопросы не отвечаю"'
# print(prompt)

response = g4f.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{"role":"user", "content":prompt}],
    stream=True,
)
generated_text = ""  # Создаем пустую переменную для сохранения текста

for message in response:
    generated_text += message  # Добавляем каждое сообщение (строку) к переменной

# Теперь в переменной generated_text содержится весь текст из response
print(generated_text)


# ### Озвучка ответа голосом Незнайки

# In[76]:


API_KEY = 'e8674ea3cacda897ad20e57e6786fa26'
set_api_key(API_KEY) 

voices = voices()
# print(voices)
voice = Voice.from_id('8AsiUYrhphlnBNuggBCK')
voice.settings.stability = 0.1
# print(voice)
audio = generate(
    text=generated_text,
    voice=voice,              
    model='eleven_multilingual_v2'
) 

with open('output.mp3', 'wb') as f:
    f.write(audio)

