from VoiceGeneratorFromText import VoiceGeneratorFromText

generator = VoiceGeneratorFromText()

# Вызов метода load_path, передавая путь к аудиофайлу
result = generator.generate_answer("Почему волна зеленая?")

# Получение результата
# print("Текст запроса:", result["request"])
print("Тема запроса:", result["topic"])
print("Эмоция запроса:", result["emotion"])
print("Путь к аудиофайлу:", result["path"])
print("Сгенерированный текст ответа:", result["answer"])
print("Лог времени:", result["timestamp"])