from django.core.files import File
from ffmpy import FFmpeg

from .models import EncodedFile, RawFile
from .util import generate_random_string


def convert_video(reference_id, encryption_key, encryption_kid):
    cache_dir = 'media/cache'
    raw_file = RawFile.objects.get(pk=reference_id)
    input_file = raw_file.raw_file.path

    # TODO: use ntpath as at https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    input_name = input_file.split('/')[-1]
    output = f'{cache_dir}/{generate_random_string()}_{input_name}'

    # Pregenerate DB entry
    encoded_file = EncodedFile(encoded_file=output, source=raw_file)
    encoded_file.encryption_key = encryption_key
    encoded_file.encryption_kid = encryption_kid
    encoded_file.save()

    ff = FFmpeg(
        inputs={input_file: None},
        outputs={
            output: f'-vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr -encryption_key {encryption_key} -encryption_kid {encryption_kid}'}
    )
    # TODO: log executed command
    # ff.cmd

    ff.run()

    encoded_file.status = 'ended'
    encoded_file.save()
