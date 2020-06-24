from rake_nltk import Rake,  Metric
from tika import parser
import requests,json
from requests import Session
from os.path import splitext
import  os
import copy
from flask import Flask, request, jsonify, render_template,session,jsonify
from werkzeug.utils import secure_filename
import nltk
from nltk.collocations import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/himanshu/auto-tag/storage'

@app.route('/')
def index():
     return "Flask app is running"


@app.route('/retrieve-tags', methods=['POST'])
def file_upload():
    files = request.files.getlist("file")
    print(request.files)
    output = []
    for file in files:
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(filename))
        extension = os.path.splitext(filename)[1]
        print('extension:',extension)
        raw = parser.from_file(filename)
        r = Rake(max_length=2)
        text = raw['content']
        r.extract_keywords_from_text(text)
        key = r.get_ranked_phrases()
        tags = []
        length = len(key)
        if length<5:
            for i in range(length):
                print("Keywords:", key[i])
                tags.append(key[i])
                x = {"id":key[i],"text":key[i],"selected":"True"}
                y = json.dumps(x)
                output.append(json.loads(y))
        elif length>=5:
            for i in range(9):
                print("Keywords:", key[i])
                tags.append(key[i])
                x = {"id":key[i],"text":key[i],"selected":"True"}
                y = json.dumps(x)
                output.append(json.loads(y))
        os.remove(os.path.join(filename))
    return jsonify({'data':output})


@app.route('/retrieve', methods=['POST'])
def retrieve_tags():
    files = request.files.getlist("file")
    print(request.files)
    tags = []
    for file in files:
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(filename))
    #    file_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        extension = os.path.splitext(filename)[1]
        print('extenion:',extension)

        if extension == ".pdf" or extension == ".docx":
            raw = parser.from_file(filename)
            r = Rake(max_length=2)
            text = raw['content']
            r.extract_keywords_from_text(text)
            key = r.get_ranked_phrases()
            length = len(key)
            if length<5:
                for i in range(length):
                    print("Keywords:", key[i])
                    tags.append(key[i])
            elif length>=5:
                for i in range(9):
                    print("Keywords:", key[i])
                    tags.append(key[i])
    return jsonify(tags)


if __name__ == "__main__":
    app.run(port=4500, debug=True)
