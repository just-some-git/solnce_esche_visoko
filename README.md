## EksmoProject - BackEnd + Data Science logic
___

### Установка в терминале для Windows

1. Клонируйте репозиторий
```commandline
git clone https://github.com/just-some-git/solnce_esche_visoko.git
```
2. Установите требуемую версию **python** из файла *pythonversion.txt*
3. Перейдите в каталог *back*, создайте и активируйте виртуальную среду
```sh
cd back
python -m venv venv
venv\scripts\activate
```
4. Установите необходимые модули
```sh
pip install -r requirements.txt
```
5. Перейдите в каталог back, создайте необходимые для проекта миграции, а затем примените их
```sh
cd back
python manage.py makemigrations
python manage.py migrate
```
___

### Запуск

Запустите сервер при помощи команды ```python manage.py runserver```
___

### Тестирование front

Для тестирования соединения используем get-запрос
  ```http://127.0.0.1:8000/question/```

Возможные ответы в формате json:

Примеры:
```json
{"status": 200, "message": "Hello!"}
```

Для отправки аудио файла используем post-запрос
  ```http://127.0.0.1:8000/questions/```

Файл прикрепляется в теле запроса в поле form-data: key - "file", value - <сам файл>

Возможные ответы:
```json
{"status": 200} - отправляется аудиофайл
{"status": 500} - ServerError
```

Для получения текста, соответствующего аудио файлу используем get-запрос
  ```http://127.0.0.1:8000/answers/<название файла с расширением>/```

Возможные ответы:
```json
{"status": 200, "filename":  <название файла>, "text":  <текст>}
{"status": 400} - BadRequest
{"status": 500} - ServerError
```
___

### Логика работы распознавания аудиофайла и генерации ответного ответа (аудио + текст)
Класс `VoiceGenerator` содержит в себе три модели машинного обучения. На вход принимает путь к аудиофайлу-запросу,
сохраняет аудиофайл-ответ и передает словарь с тремя ключами:

- __"answer_path"__ - путь к директории с ответом
- __"answer_name"__ - уникальное имя аудио-ответа
- __"answer_text"__ - сгенерированный транскрипт

Используемые библиотеки whisper, elevenlabs, g4f, os, datetime загружаются при обращении к файлу
`__init__.py`, который загружает модели машинного обучения, чтения голоса и голос диктора для последующей генерации
при инициализации объекта класса.

`_get_unique_filename` - приватный метод класса генерации уникального имени файла и пути к файлу.

`load_path` - публичный метод класса, принимающий на вход путь к аудиофайлу-запросу в строковом варианте
и возвращающий словарь с указанием пути к файлу-ответу и текстом запроса.
Модель whisper считывает аудиофайл-запрос и переводит его в текст.
Полученный запрос в текстовом варианте передается в модель g4f, где при помощи генеративного предобученного
трансформера подготавливается ответ в текстовом варианте. Далее текстовый вариант ответа переводится в аудиофайл
и сохраняется под уникальным названием в указанной в настройках проекта директории.
___

### Пример использования:

Создание экземпляра класса `VoiceGenerator`:

`generator = VoiceGenerator()`

Вызов метода `load_path`, передавая путь к аудиофайлу:

`result = generator.load_path("путь_к_вашему_аудиофайлу.wav")`

Визуализация результата:

`print("Путь к аудиофайлу:", result["path"])`\
`print("Сгенерированный текст:", result["answer"]`
___

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
   parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json'],
    tsconfigRootDir: __dirname,
   },
```

- Replace `plugin:@typescript-eslint/recommended` to `plugin:@typescript-eslint/recommended-type-checked` or `plugin:@typescript-eslint/strict-type-checked`
- Optionally add `plugin:@typescript-eslint/stylistic-type-checked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and add `plugin:react/recommended` & `plugin:react/jsx-runtime` to the `extends` list
