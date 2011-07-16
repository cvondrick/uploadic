import os.path, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from turkic.server import handler, application
from turkic.database import session
from models import *
from vision import ffmpeg

# public/javascript.js will call this in order to get the activities for this
# particular job. we return a list of attributes here. the framework will
# automatically handle the conversion from python to javascript for us.
@handler()
def getjob(id):
    # the database is called session
    job = session.query(Job).get(id)
    activities = [x.text for x in job.activities]
    return {"activities": activities}

# this method is called through apache when we upload a video. this will 
# read the HTTP protocol and figure out how to handle the file uploads.
# it is a little complicated, but the basic idea is to extract the useful
# bits and store it. finally, we must notify the client that the upload was
# successful so the web browser can redirect.
@handler("text/html", environ = True)
def upload(id, environ):
    job = session.query(Job).get(id)
    data = environ["wsgi.input"]

    # read meta data first
    header = data.readline().strip() + "--"
    while True:
        chunk = data.readline()
        if chunk.strip() == "":
            break
        key, value = chunk.split(": ", 1)
        if key == "Content-Type":
            job.mimetype = value.strip()
        if key == "Content-Disposition":
            for item in value.split("; "):
                itemdata = item.split("=", 1)
                if len(itemdata) == 2 and itemdata[0] == "filename":
                    job.filename = itemdata[1].strip()[1:-1]
    session.commit()

    # now read the file data, looking for the terminating sequence
    out = open(job.storepath, "wb")
    while True:
        chunk = data.readline(1024 * 1024)
        if chunk.strip() == header:
            break
        out.write(chunk)
    out.close()

    return ["<script>parent.uploaded();</script>"]
