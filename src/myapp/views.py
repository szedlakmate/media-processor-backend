import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .convert_video import convert_video
from .forms import DocumentForm
from .models import RawFile


@csrf_exempt
def upload_file(request):
    message = 'Upload as many files as you want!'

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = RawFile(raw_file=request.FILES['docfile'])
            newdoc.save()

            return HttpResponse(f'reference_id: {newdoc.id}', content_type="text/plain")

        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = RawFile.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)


@csrf_exempt
def package_content(request):
    # Package content
    if request.method == 'POST':
        # TODO: handle bad requests
        data = json.loads(request.body)
        reference_id = data['reference_id']
        key = data['key']
        kid = data['kid']
        # encryption_key = '76a6c65c5ea762046bd749a2e632ccbb'
        # encryption_kid = 'a7e61c373e219033c21091fa607bf3b8'
        convert_video(reference_id=reference_id, encryption_key=key, encryption_kid=kid)
        return HttpResponse(f'id: {reference_id}, key: {key}, kid: {kid}')

    return HttpResponse("Ho")
