from ffmpy import FFmpeg


def convert_video():
    location = 'media/'
    input_file = f'{location}test.mp4'
    output_file = f'{location}test_encrypted.mp4'
    encryption_key = '76a6c65c5ea762046bd749a2e632ccbb'
    encryption_kid = 'a7e61c373e219033c21091fa607bf3b8'

    ff = FFmpeg(
        inputs={input_file: None},
        outputs={
            output_file: f'-vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr -encryption_key {encryption_key} -encryption_kid {encryption_kid}'}
    )
    # TODO: log executed command
    # ff.cmd

    ff.run()
