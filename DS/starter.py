from VoiceGenerator import VoiceGenerator

generator = VoiceGenerator()

# Вызов метода load_path, передавая путь к аудиофайлу
result = generator.generate_answer("Почему небо голубое?")

# Получение результата
print(result)