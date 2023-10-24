from VoiceGenerator import VoiceGenerator

generator = VoiceGenerator()

# Вызов метода load_path, передавая путь к аудиофайлу
result = generator.load_path("hny.wav")

# Получение результата
print("Путь к аудиофайлу:", result["path"])
print("Сгенерированный текст:", result["answer"])