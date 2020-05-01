from threading import Thread

from ffmpy import FFmpeg

from .models import EncodedFile, RawFile
from .util import generate_random_string


def consume_video(reference_id, encryption_key, encryption_kid):
    target_dir = 'media/repacked'
    raw_file = RawFile.objects.get(pk=reference_id)
    input_file = raw_file.raw_file.path

    # TODO: use ntpath as at https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    input_name = input_file.split('/')[-1]
    output = f'{target_dir}/{generate_random_string()}_{input_name}'

    # Pre-generate DB entry
    encoded_file = EncodedFile(encoded_file=output, source=raw_file)
    encoded_file.encryption_key = encryption_key
    encoded_file.encryption_kid = encryption_kid
    encoded_file.save()

    thread = Thread(target=convert_video, args=(input_file, output, encoded_file.id))
    thread.start()

    return encoded_file.id


def convert_video(input_file, output, encode_file_id):
    encoded_file = EncodedFile.objects.get(id=encode_file_id)

    try:
        ff = FFmpeg(
            inputs={input_file: None},
            outputs={
                output: f'-vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr -encryption_key {encoded_file.encryption_key} -encryption_kid {encoded_file.encryption_kid}'}
        )
        # TODO: log executed command
        # ff.cmd

        ff.run()

        encoded_file.status = 'ended'
        encoded_file.save()

    except Exception:
        encoded_file.status = 'failed'
        encoded_file.save()
