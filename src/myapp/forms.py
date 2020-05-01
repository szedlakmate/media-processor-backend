from django import forms


class DocumentForm(forms.Form):
    media_file = forms.FileField(label='Select a file')
