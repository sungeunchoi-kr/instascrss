import os
from flask import Flask, Response, request
from flask_restful import Resource, Api
from waitress import serve
import base64

from snapshotter import Snapshotter

app = Flask(__name__)
api = Api(app)

snap = Snapshotter()

##### begin api route definitions #####
@app.route('/api/take-snapshot/<urlId>', methods=['POST'])
def takeSnapshots(urlId):
    print('POST /api/take-snapshot/<urlId>: got urlId=' + urlId)
    filename = '/tmp/' + urlId + '.png'
    snap.snapshot_post(urlId, filename)

    # read back the file as base64
    with open(filename, 'rb') as file:
        data = base64.b64encode(file.read())

    try:
        os.remove(filename)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    return { 'data': data }

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    serve(app, host='0.0.0.0', port=port)

