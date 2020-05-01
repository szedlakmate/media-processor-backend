from django.db import models

CONVERSION_STATUS = (
    ('init', 'initiated'),
    ('ended', 'finished')
)


class RawFile(models.Model):
    raw_file = models.FileField(upload_to='uploaded/%Y/%m/%d')


class EncodedFile(models.Model):
    source = models.ForeignKey(RawFile, on_delete=models.CASCADE)
    encoded_file = models.FileField(upload_to='encoded')
    encryption_key = models.TextField()
    encryption_kid = models.TextField()
    status = models.TextField(choices=CONVERSION_STATUS, default='init')
