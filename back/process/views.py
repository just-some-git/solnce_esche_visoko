import os.path

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse,
    FileResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseBase,
    HttpRequest,
)

from back.settings import MEDIA_ROOT_QUESTIONS
from .models import Question, Answer
from DS.VoiceGenerator import VoiceGenerator


generator = VoiceGenerator()


def create_response(output_json: dict, pk: int) -> HttpResponseBase:
    try:
        path = output_json['answer_path']
        filename = output_json['answer_name']
        text = output_json['answer_text']
    except KeyError as e:
        return HttpResponseServerError('Invalid or missing JSON key: %s' % e)

    quest = get_object_or_404(
        klass=Question,
        id=pk,
    )
    Answer.objects.create(
        audio_path=path,
        audio_name=filename,
        text=text,
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
def question(request: HttpRequest) -> HttpResponseBase:
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
        file_path = os.path.abspath(os.path.join(MEDIA_ROOT_QUESTIONS, input_file))

        new_question = Question.objects.create(
            audio_path=MEDIA_ROOT_QUESTIONS,
            audio_name=file.name,
        )
        new_question_id = new_question.pk

        try:
            result = generator.load_path(path=file_path)
        except FileNotFoundError as e:
            return HttpResponseServerError('Cannot find file: %s' % e)

        response = create_response(
            output_json=result,
            pk=new_question_id,
        )

        return response


def answer_text(request: HttpRequest, answer_id: str) -> HttpResponseBase:
    if request.method == 'GET':
        try:
            ans = get_object_or_404(
                klass=Answer,
                audio_name=answer_id,
            )
        except MultipleObjectsReturned as e:
            return HttpResponseServerError(e)

        if ans:
            data = {
                'filename': answer_id,
                'text': ans.text,
            }

            return JsonResponse(
                status=200,
                data=data,
                safe=False,
            )

    return HttpResponseBadRequest()
