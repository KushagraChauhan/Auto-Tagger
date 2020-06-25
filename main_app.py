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

'''
Default route- This route is used to check whether the app is running or not
'''
@app.route('/')
def index():
     return "Flask app is running"

'''
Retrieve tags from a file in specified format-

Flow-
Input- Files
Processing on the files
Output - Tags in specified format

Explanation-
    1. Upload the files via POST method to the given url
    2. A for loop will iterate over all the files uploaded
    3. Files are saved in the given path
    4. Extension of the file is determined
    5. Tika Server is used to parse the text from the Files
    6. After the extraction of text, rake-nltk is used to extract the Keywords
    7. The Keywords are returned in the specified format
'''
@app.route('/v1/retrieve-tags', methods=['POST'])
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
        rake_var = Rake(max_length=2)
        text = raw['content']
        rake_var.extract_keywords_from_text(text)
        key = rake_var.get_ranked_phrases()
        tags = []
        length = len(key)
        if length<5:
            for i in range(length):
                print("Keywords:", key[i])
                tags.append(key[i])
                list1 = {"id":key[i],"text":key[i],"selected":"True"}
                list2 = json.dumps(list1)
                output.append(json.loads(list2))
        elif length>=5:
            for i in range(9):
                print("Keywords:", key[i])
                tags.append(key[i])
                list1 = {"id":key[i],"text":key[i],"selected":"True"}
                list2 = json.dumps(list1)
                output.append(json.loads(list2))
        os.remove(os.path.join(filename))
    return jsonify({'data':output})

'''
Retrieve tags from a file-

Flow-
Input- Files
Processing on the files
Output - Tags in specified format

Explanation-
    1. Upload the files via POST method to the given url
    2. A for loop will iterate over all the files uploaded
    3. Files are saved in the given path
    4. Extension of the file is determined
    5. Tika Server is used to parse the text from the Files
    6. After the extraction of text, rake-nltk is used to extract the Keywords
'''

@app.route('/v1/retrieve', methods=['POST'])
def retrieve_tags():
    files = request.files.getlist("file")
    print(request.files)
    tags = []
    for file in files:
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(filename))
        #file_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        extension = os.path.splitext(filename)[1]
        print('extenion:',extension)
        raw = parser.from_file(filename)
    #    raw = parser.from_file('/home/himanshu/auto-tag/storage/'+filename)
        rake_var = Rake(max_length=2)
        text = raw['content']
        rake_var.extract_keywords_from_text(text)
        key = rake_var.get_ranked_phrases()
        length = len(key)
        if length<5:
            for i in range(length):
                print("Keywords:", key[i])
                tags.append(key[i])
        elif length>=5:
            for i in range(9):
                print("Keywords:", key[i])
                tags.append(key[i])
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))

    return jsonify(tags)


if __name__ == "__main__":
    app.run(port=4500, debug=True)
