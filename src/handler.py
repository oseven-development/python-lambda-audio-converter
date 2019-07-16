import subprocess
import base64
import json
import datetime

# os.system("cp ffmpeg /tmp") os.system("chmod 775 /tmp/ffmpeg")

audio = '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'

FFMPEG_STATIC = "/var/task/ffmpeg"


def converter(event, context):
    # decode audio
    # ! hier muss noch der event context hin
    decoded_audio = base64.b64decode(event['body'])
    # erstellt .m4a
    with open('/tmp/audio.m4a', 'wb') as file_:
        file_.write(decoded_audio)
    # converter es
    subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a", "-f",
                    "flac", "/tmp/fileout.flac", "-y"])
    # erstell flac
    with open("/tmp/fileout.flac", "rb") as audio_file:
        encoded_flac = base64.b64encode(audio_file.read())
    # erstellt response
    res = {
        "statusCode": 200,
        "body": json.dumps(encoded_flac.decode("utf-8"))
    }

    return res
