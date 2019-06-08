from flask import Flask, request, Response, jsonify, json, send_file
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
    pic = to_img(request, 'picture')
    carrier_img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], "carrier.png"))  
    steg = lsbrick(carrier_img, 16)
    try:
        res = steg.encode_image(pic)
        res_file = cv2.imwrite("result.png", res)
        if(res_file == False):
            raise ValueError('Failed to convert image. Please try again')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        app.logger.info(res)
        return send_file(filename_or_fp=dir_path + "/result.png", mimetype="image/gif", as_attachment=True)
    except ValueError as e:
        response = {'err': str(e)}
        response_pickled = jsonify(response)
        return Response(json.dumps(response), mimetype=u'application/json') 

@app.route('/api/image_decode', methods=['POST'])
def decode():
    # if receive a carrier, it's been encoded already
    carrier_img = to_img(request, 'encoded_img')
    steg = lsbrick(carrier_img, 16)
    try:
        orig_img = steg.decode_image()
        res_file = cv2.imwrite("original.png", orig_img)
        if(res_file == False):
            raise ValueError('Failed to decode image. Please try again')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return send_file(filename_or_fp=dir_path + "/original.png", mimetype="image/gif", as_attachment=True)
    except ValueError as e:
        response = {'err': str(e)}
        response_pickled = jsonify(response)
        return Response(json.dumps(response), mimetype=u'application/json') 

@app.route('/api/text_encode', methods=['POST'])
def t_encode():
    carrier_img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], "bryan_michael.png"))  
    steg = lsbrick(carrier_img, 16)
    try:
        body = request.json
        print(body['text'])
        res = steg.encode_text(body['text'])
        res_file = cv2.imwrite("result.png", res)
        if(res_file == False):
            raise ValueError('Failed to convert text. Please try again')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        app.logger.info(res)
        return send_file(filename_or_fp=dir_path + "/result.png", mimetype="image/gif", as_attachment=True)
    except ValueError as e:
        response = {'err': str(e)}
        response_pickled = jsonify(response)
        return Response(json.dumps(response), mimetype=u'application/json') 

@app.route('/api/text_decode', methods=['POST'])
def t_decode():
    # if receive a carrier, it's been encoded already
    carrier_img = to_img(request, 'encoded_img')
    steg = lsbrick(carrier_img, 16)
    try:
        orig_text = steg.decode_text()
        print(orig_text)
        res_file = open('decoded_text.txt', "w+")
        res_file.write(orig_text)
        if(not res_file):
            raise ValueError('Failed to decode image. Please try again')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return send_file(filename_or_fp=dir_path + "/decoded_text.txt", mimetype="text/*", as_attachment=True)
    except ValueError as e:
        response = {'err': str(e)}
        response_pickled = jsonify(response)
        return Response(json.dumps(response), mimetype=u'application/json') 

# start flask app
app.debug = True
app.run(host="0.0.0.0", port=5000)
