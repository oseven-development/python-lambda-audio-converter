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
    print(event)
    headers = event['headers']
    body = event['body']

    ctype, pdict = cgi.parse_header(headers['content-type'])

    if ctype == 'multipart/form-data':
        pdict['CONTENT-LENGTH'] = int(headers['content-length'])

        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        b = bytes(body, 'iso-8859-1')
        fields = cgi.parse_multipart(BytesIO(b), pdict)

        out = open('/tmp/audio.m4a', 'w+b')
        out.write(fields['data'][0])
        out.close()

        tmp_file = open('/tmp/fileout.flac', 'w+')
        tmp_file.close()

    subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a",
                "-f", "flac", "/tmp/fileout.flac", "-y"])

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

    return res

# os.system("cp ffmpeg /tmp") os.system("chmod 775 /tmp/ffmpeg")



    # print(form_data)

    # print(file)
    # with open("request.txt", "w+") as audio_file:
    #     audio_file.write(json.dumps(event))
    
    # with open("request.m4a", "wb") as audio_file:
    #     audio_file.write(event['body'])
    # data = json.loads(event['body'])
    # Let's say we user a regular <input type='file' name='uploaded_file'/>
    # encoded_file = data['uploaded_file']
    # decoded_file = base64.decodestring(encoded_file)

    # req = json.loads(event)['body']['audio']
    # print(req)
    # print(data)
    # print(req)
    # print(type(req))
    # print(req)
    # print(event['body']['body'])
    # print(event['body'])
    # decoded_audio = base64.b64decode(req)
    # erstellt .m4a
    # with open('/tmp/audio.m4a', 'wb') as file_:
    #     file_.write(decoded_audio)
    # file_.close()
    # temp file
    # tmp_file = open('/tmp/fileout.flac', 'w+')
    # tmp_file.close()

    # # converter es
    # subprocess.run([FFMPEG_STATIC, "-i", "/tmp/audio.m4a", "-f",
    #                 "flac", "/tmp/fileout.flac", "-y"])
    # # erstell flac
    # with open("/tmp/fileout.flac", "rb") as audio_file:
    #     encoded_flac = base64.b64encode(audio_file.read())
    # audio_file.close()
    # # removed file for new funktion call
    # # erstellt response
    # print(encoded_flac)
    # res = {
    #     "statusCode": 200,
    #     "headers": {
    #         "Content-Type": "application/json",
    #         "Access-Control-Allow-Origin": "*"
    #     },
    #     "body": json.dumps(encoded_flac.decode("utf-8"))
    # }
    # os.remove("/tmp/fileout.flac")
    # os.remove("/tmp/audio.m4a")
