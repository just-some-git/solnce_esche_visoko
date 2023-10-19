Backend - часть проекта

Установка в терминале для Windows

1. Клонируйте репозиторий
```commandline
git clone https://github.com/just-some-git/solnce_esche_visoko.git
```
2. Установите требуемую версию **python** из файла *pythonversion.txt*
3. Перейдите в каталог *back*, создайте и активируйте виртуальную среду
```sh
cd passes_base
python -m venv venv
venv\scripts\activate
```
4. Установите необходимые модули
```sh
pip install -r requirements.txt
cd back
```

Запуск

Запустите сервер при помощи команды ```python manage.py runserver```

Тестирование front

Для тестирования соединения используем get-запрос
  ```http://127.0.0.1:8000/question/```

Возможные ответы в формате json:
Примеры:
```json
{"status": 200, "message": "Hello!"}
```

Для отравки аудио файла используем post-запрос
  ```http://127.0.0.1:8000/question/```

Файл прикрепляется в поле form-data: key - <file>, value - <сам файл>

Возможные ответы:
```json
{"status": 200} - отправляется аудиофайл
{"status": 500} - ServerError
```

Для получения текта, соответствующего аудио файлу используем get-запрос
  ```http://127.0.0.1:8000/answer/<название файла с расширением>```
Возможные ответы:
```json
{"status": 200, "filename":  <название файла>, "text":  <текст>}
{"status": 400} - BadRequest
{"status": 500} - ServerError
```

Тестирование DS

Для тестирования необходимо заменить строку в файле views.py с вызовом метода
входной аргумент метода input_file - текстовая строка с путем до файла
выходные параметры метода output_json в формате {'path': <путь до файла>, 'audio': <имя файла>, 'text': <разбивка по времени>}