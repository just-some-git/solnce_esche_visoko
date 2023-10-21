from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse,
    FileResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)

from back.settings import *
from .models import Question, Answer


def create_response(output_json, quest):
    try:
        path = output_json['path']
        filename = output_json['audio']
        text = output_json['text']
        t_f = output_json['time-frames']
    except KeyError as e:
        return HttpResponseServerError('Invalid or missing JSON key: %s' % e)

    Answer.objects.create(
        audio_path=path,
        audio_name=filename,
        text=text,
        time_frames=t_f,
        question=quest,
    )

    response = FileResponse(
        open(
            file=path + filename,
            mode='rb',
        ),
        filename=filename,
    )
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['X-Sendfile'] = filename

    return response


@csrf_exempt
def question(request):
    if request.method == 'GET':
        return JsonResponse(
            status=200,
            data={'message': 'Hello!'},
        )
    if request.method == 'POST':
        try:
            file = request.FILES['file']
        except KeyError as e:
            return HttpResponseServerError('Invalid or missing header: %s' % e)

        fs = FileSystemStorage(location=MEDIA_ROOT_QUESTIONS)
        input_file = fs.save(
            name=file.name,
            content=file,
        )
        new_question = Question.objects.create(
            audio_path=MEDIA_ROOT_QUESTIONS,
            audio_name=file.name,
        )

        """
            TODO: здесь должен быть вызов DS-метода с аргументом input_file
            input_file - текстовая строка с путем до файла
            формат json ответа от DS-метода:
            {
                "path": "<путь до аудиофайла>",
                "audio": "<имя аудиофайла>",
                "text": "<просто текст ответа>",
                "time-frames": "<разбивка по тайм-фреймам 12 (или сколько угодно) fps>"
            }
            """

        output_json = {
            'path': MEDIA_ROOT_ANSWERS,
            'audio': 'example.mp3',
            'text': 'example text',
            'time-frames': {
                "шла": "Саша",
                "по": "шоссе",
                "и": "сосала",
                "сушку": "вот",
            },
        }
        response = create_response(
            output_json=output_json,
            quest=new_question,
        )
        return response


def answer_text(request, answer_id):
    if request.method == 'GET':
        try:
            ans = get_object_or_404(
                klass=Answer,
                audio_name=answer_id,
            )
        except MultipleObjectsReturned as e:
            return HttpResponseServerError(e)

        if ans:
            return JsonResponse(
                status=200,
                data={
                    'filename': answer_id,
                    'text': ans.text,
                },
            )

    return HttpResponseBadRequest()
