from flask import Flask, request, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import jsonpickle
import numpy as np
import cv2
import os

from kubrick import lsbrick

# Initialize the Flask application
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'bin', 'png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def to_img(request, key):
    f = request.files[key]
    app.logger.info(f)
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), buffer_size=16384000)
    f.close()
    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
    return img

def store_carrier(request):
    carrier_img = to_img(request, 'carrier')
    steg = lsbrick(carrier_img, 16)
    return steg

# route http posts to this method
@app.route('/api/image_encode', methods=['POST'])
def encode():
    pic = to_img(request, 'pic')
    steg = store_carrier(request)
    new_img = steg.encode_image(pic)
    app.logger.info(new_img)

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(1,1)
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/image_decode', methods=['POST'])
def decode():
    steg = store_carrier(request)
    orig_im = steg.decode_image()

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.debug = True
app.run(host="0.0.0.0", port=5000)
