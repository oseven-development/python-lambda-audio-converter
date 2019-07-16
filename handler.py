import subprocess
import base64
import json
import datetime
import os

# os.system("cp ffmpeg /tmp") os.system("chmod 775 /tmp/ffmpeg")

FFMPEG_STATIC = "/var/task/ffmpeg"


def converter(event, context):
    # decode audio
    # ! hier muss noch der event context hin
    decoded_audio = base64.b64decode(event['body'])
    # create placeholder files
    subprocess.call(['touch', '/tmp/audio.m4a'])
    subprocess.call(['touch', '/tmp/fileout.flac'])

    # erstellt .m4a
    with open('/tmp/audio.m4a', 'wb') as file_:
        file_.write(decoded_audio)
    # converter es
    subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a", "-f",
                    "flac", "/tmp/fileout.flac", "-y"])
    # erstell flac
    with open("/tmp/fileout.flac", "rb") as audio_file:
        encoded_flac = base64.b64encode(audio_file.read())
    # removed file for new funktion call
    os.remove("/tmp/fileout.flac")
    os.remove("/tmp/audio.m4a")

    # erstellt response
    res = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(encoded_flac.decode("utf-8"))
    }

    return res
