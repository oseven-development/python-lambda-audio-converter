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

    if ctype == 'multipart/form-data':
        pdict['CONTENT-LENGTH'] = int(headers['Content-Length'])

        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        b = bytes(body, 'iso-8859-1')
        fields = cgi.parse_multipart(BytesIO(b), pdict)

        out = open('audio.m4a', 'w+b')
        out.write(fields['data'][0])
        out.close()

        tmp_file = open('fileout.flac', 'w+')
        tmp_file.close()

        subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a",
                        "-f", "flac", "/tmp/fileout.flac", "-y"])

        # os.remove("/tmp/fileout.flac")
        # os.remove("/tmp/audio.m4a")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": "file"
    }
