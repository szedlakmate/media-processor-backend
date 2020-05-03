import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .convert_video import consume_video
from .forms import DocumentForm
from .models import RawFile, EncodedFile


def upload_file(request):
    """
    Manages file upload (RawFile)
    :param request:
    :return: POST: reference_id GET: index.html'
    """
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = RawFile(raw_file=request.FILES['media_file'])
            newfile.save()

            return HttpResponse(f'reference_id: {newfile.id}', content_type="text/plain")

    else:
        form = DocumentForm()  # An empty, unbound form

    # Render upload page
    context = {'form': form}
    return render(request, 'index.html', context)


@csrf_exempt
def packaged_content(request):
    """
    Start RawFile packaging background task
    :param request:
    :return: POST: packaged_content_id
    """
    # Package content
    if request.method == 'POST':
        # TODO: handle bad requests
        data = json.loads(request.body)
        reference_id = data['reference_id']
        key = data['key']
        kid = data['kid']
        converted_file_id = consume_video(reference_id=reference_id, encryption_key=key, encryption_kid=kid)
        return HttpResponse(f'packaged_content_id: {converted_file_id}')

    return HttpResponseBadRequest("Only post requests are allowed")


@csrf_exempt
def packaged_content_status(request, packaged_content_id):
    """
    Response status of the initiated file packaging task.
    Responses:
        200: finished
        202: Encoding has started
        404: EncodedFile.id not found
        500: Encoding failed
    :param request:
    :param packaged_content_id: EncodedFile.id
    :return: response status of EncodedFile packaging process
    """
    if request.method == 'GET':
        try:
            encoded_file = EncodedFile.objects.get(id=packaged_content_id)
        except Exception:
            return HttpResponse('Referenced item is not found', status=404)
        if encoded_file.status == 'init':
            return HttpResponse('Processing has been started', status=202)
        elif encoded_file.status == 'ended':
            return HttpResponse(
                f'location: {encoded_file.encoded_file.url}, key: {encoded_file.encryption_key}, kid: {encoded_file.encryption_kid}',
                status=200)
        elif encoded_file.status == 'failed':
            return HttpResponse('Processing the file failed', status=500)

    return HttpResponseBadRequest("Only GET requests are allowed")
