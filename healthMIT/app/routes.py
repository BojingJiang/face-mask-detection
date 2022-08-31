from flask import render_template
from flask import request
from app import app

import sys
import os
import dlib
import glob

predictor_path = 'app/nose.dat'

def nose_detected(imgfile):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    img = dlib.load_rgb_image(imgfile)
    dets = detector(img, 1)

    print("# nose detected: {}".format(len(dets)))
    if dets:
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html', result='Please Upload an image with a masked face')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    img = request.files['imgfile']
    dotname = img.filename.split('.')[-1]
    name='temp.' + dotname
    img.save(name)
    nose = nose_detected(name)
    if nose:
        prompt = 'We have detected an uncovered nose in this image.'
    else:
        prompt = 'We have not detected an uncovered nose in this image.'

    return render_template('index.html', result=prompt)

