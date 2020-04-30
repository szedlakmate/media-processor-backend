import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import DocumentForm
from .models import Document


@csrf_exempt
def upload_file(request):
    message = 'Upload as many files as you want!'

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return HttpResponse(f'reference_id: {newdoc.id}', content_type="text/plain")

        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

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
        return HttpResponse(f'id: {reference_id}, key: {key}, kid: {kid}')

    return HttpResponse("Ho")
