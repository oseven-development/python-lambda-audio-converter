import subprocess
import base64
import json
import datetime
import os
import cgi
from io import BytesIO


# os.system("cp ffmpeg /tmp") os.system("chmod 775 /tmp/ffmpeg")

FFMPEG_STATIC = "/var/task/ffmpeg"


def converter(event, context):

    headers = event['headers']
    body = event['body']

    ctype, pdict = cgi.parse_header(headers['Content-Type'])
    # print(pdict)
    pdict['CONTENT-LENGTH'] = int(headers['Content-Length'])

    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

    b = bytes(body, 'utf-8')
    fields = cgi.parse_multipart(BytesIO(b), pdict)
    # print(fields['data'][0])
    out = open('audio.mp4', 'w+b')
    out.write(fields['data'][0])
    out.close()
    print("-----------------------------")
    # print(pdict)

    # print(fields)
    # if ctype == 'multipart/form-data':
    #     fields = cgi.parse_multipart(body, pdict)
    # messagecontent = fields.get('message')


def converter2(event, context):
    print(event)
    # decode audio
    # print(event)
    req = json.loads(event)['body']['audio']
    print(req)
    # print(data)
    # print(req)
    # print(type(req))
    # print(req)
    # print(event['body']['body'])
    # print(event['body'])
    decoded_audio = base64.b64decode(req)
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

    # print(res)
    return res


#
