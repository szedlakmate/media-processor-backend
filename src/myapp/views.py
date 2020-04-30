from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Document
from .forms import DocumentForm


def my_view(request):
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
