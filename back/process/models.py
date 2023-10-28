from django.db import models


class Question(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    audio_path = models.TextField(
        help_text='Путь до директории, хранящей аудиозапись вопроса пользователя',
        verbose_name='Директория',
    )
    audio_name = models.CharField(
        max_length=255,
        help_text='Имя аудиофайла вопроса пользователя',
        verbose_name='Имя',
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} - {self.audio_path}{self.audio_name}'


class Answer(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    audio_path = models.TextField(
        help_text='Путь до директории, хранящей аудиозапись ответа персонажа',
        verbose_name='Директория',
    )
    audio_name = models.CharField(
        max_length=255,
        help_text='Имя аудиофайла ответа персонажа',
        verbose_name='Имя',
    )
    text = models.TextField(
        help_text='Текст ответа персонажа',
        verbose_name='Текст',
    )
    question = models.OneToOneField(
        to=Question,
        on_delete=models.CASCADE,
        related_name='to_question',
        verbose_name='Вопрос'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} - {self.audio_path}{self.audio_name}'
