import os.path

from datetime import datetime
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

from back.settings import MEDIA_ROOT_QUESTIONS, MEDIA_ROOT_ANSWERS
from .models import Question, Answer
# from DS.VoiceGenerator import VoiceGenerator


# generator = VoiceGenerator()


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
        audio_name=filename.split(sep='.')[0],  # TODO: исправить этот костыль
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
    # response['X-Sendfile'] = filename
    return response


@csrf_exempt
def question(request: HttpRequest) -> HttpResponseBase:
    if request.method == 'GET':
        return JsonResponse(
            status=200,
            data={
                'status': 200,
                'message': 'Hello!',
            },
        )
    if request.method == 'POST':
        try:
            # name = request.POST['name']
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            wav_name = now + '.wav'
            file = request.FILES['audio']
        except KeyError as e:
            return HttpResponseServerError('Invalid or missing field: %s' % e)

        input_fs = FileSystemStorage(location=MEDIA_ROOT_QUESTIONS)
        input_file = input_fs.save(
            name=wav_name,
            content=file,
        )
        # file_path = os.path.abspath(os.path.join(MEDIA_ROOT_QUESTIONS, input_file))

        new_question = Question.objects.create(
            audio_path=MEDIA_ROOT_QUESTIONS,
            audio_name=wav_name,
        )
        new_question_id = new_question.pk

        output_fs = FileSystemStorage(location=MEDIA_ROOT_ANSWERS)
        output_file = output_fs.save(
            name=wav_name,
            content=file,
        )

        # try:
        #     result = generator.load_path(
        #         path=file_path,
        #         filename=name,
        #     )
        # except FileNotFoundError as e:
        #     return HttpResponseServerError('Cannot find file: %s' % e)

        result = {
            "answer_path": MEDIA_ROOT_ANSWERS,
            "answer_name": wav_name,
            "answer_text": f"generated_text_{now}",
        }

        response = create_response(
            output_json=result,
            pk=new_question_id,
        )
        return response
    return HttpResponseBadRequest()


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
                'filename': answer_id + '.wav',
                'text': ans.text,
            }
            return JsonResponse(
                status=200,
                data=data,
                safe=False,
            )
    return HttpResponseBadRequest()
