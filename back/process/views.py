from django.http import JsonResponse, FileResponse, HttpResponseBadRequest, HttpResponseServerError
from back.settings import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

__files = {}

def create_response(output_json):
    filename = output_json['audio']
    path = output_json['path']
    text = output_json['text']
    __files[filename] = text

    response = FileResponse(open(path + filename, 'rb'), filename=filename)
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['X-Sendfile'] = filename

    return response

@csrf_exempt
def question(request):
    if request.method == 'GET':
        return JsonResponse(status=200, data={'message': 'Hello!'})
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            fs = FileSystemStorage(location=MEDIA_ROOT_QUESTIONS)
            input_file = fs.save(file.name, file)

            """
            TODO: здесь должен быть вызов DS-метода с аргументом input_file
            input_file - текстовая строка с путем до файла
            формат json ответа от DS-метода:
            {'path': <путь до файла>, 'audio': <имя файла>, 'text': <разбивка по времени>}
            """

            output_json = {'path': MEDIA_ROOT_ANSWERS, 'audio': 'example.mp3', 'text': 'example text'}
            response = create_response(output_json)
            return response
        except:
            return HttpResponseServerError()

def answer_text(request, answer_id):
    if request.method == 'GET':
        if answer_id in __files.keys():
            return JsonResponse(status=200, data={'filename': answer_id, 'text': __files[answer_id]})
        else:
            return HttpResponseServerError()

    return HttpResponseBadRequest()
