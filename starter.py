from VoiceGeneratorFromText import VoiceGeneratorFromText

generator = VoiceGeneratorFromText()

# Вызов метода load_path, передавая путь к аудиофайлу
result = generator.generate_answer("почему пилюлькин такой вредный?")

# Получение результата
print("Тема запроса:", result["topic"])
print("Эмоция запроса:", result["emotion"])
print("Путь к аудиофайлу:", result["path"])
print("Сгенерированный текст ответа:", result["answer"])
print("Лог времени:", result["timestamp"])