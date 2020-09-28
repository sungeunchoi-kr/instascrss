import os
from datetime import datetime
from pathlib import Path
from flask import Flask, Response, request
from flask_restful import Resource, Api
from waitress import serve
import base64

from snapshotter import Snapshotter

rootdir = os.environ.get('ROOTDIR') or './post-snapshots'

app = Flask(__name__)
api = Api(app)

snap = Snapshotter()

##### begin api route definitions #####
@app.route('/api/take-snapshot/<urlId>', methods=['POST'])
def takeSnapshots(urlId):
    print('POST /api/take-snapshot/<urlId>: got urlId=' + urlId)

    now = datetime.now()
    subdir = now.strftime("%Y%m")
    date_time = now.strftime("%Y%m%dT%H%M%S")

    filename = urlId + '-' + date_time + '.png'
    uri = subdir + '/' + filename
    filepath = rootdir + '/' + uri

    Path(rootdir + '/' + subdir).mkdir(parents=True, exist_ok=True)
    snap.snapshot_post(urlId, filepath)

    return { 'uri': uri }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    serve(app, host='0.0.0.0', port=port)

