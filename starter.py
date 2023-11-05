from VoiceGenerator import VoiceGenerator

generator = VoiceGenerator()

# Вызов метода load_path, передавая путь к аудиофайлу
result = generator.load_path("hny.wav")

# Получение результата
print("Считанный текст запроса:", result["request"])
print("Тема запроса:", result["topic"])
print("Эмоция запроса:", result["emotion"])
print("Путь к аудиофайлу:", result["path"])
print("Сгенерированный текст ответа:", result["answer"])