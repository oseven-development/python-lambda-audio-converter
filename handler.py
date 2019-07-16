import subprocess
import base64
import json
import datetime
import os
# os.system("cp ffmpeg /tmp") os.system("chmod 775 /tmp/ffmpeg")

FFMPEG_STATIC = "/var/task/ffmpeg"


def converter(event, context):
    # decode audio
    print(event['body'])
    # print(event['body'])
    decoded_audio = base64.b64decode(event['body'])
    # erstellt .m4a
    with open('/tmp/audio.m4a', 'wb') as file_:
        file_.write(decoded_audio)
    file_.close()
    # temp file
    tmp_file = open('/tmp/fileout.flac', 'w+')
    tmp_file.close()

    # converter es
    subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a", "-f",
                    "flac", "/tmp/fileout.flac", "-y"])
    # erstell flac
    with open("/tmp/fileout.flac", "rb") as audio_file:
        encoded_flac = base64.b64encode(audio_file.read())
    audio_file.close()
    # removed file for new funktion call
    # erstellt response
    res = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(encoded_flac.decode("utf-8"))
    }
    os.remove("/tmp/fileout.flac")
    os.remove("/tmp/audio.m4a")
    print(res)
    return res


#
