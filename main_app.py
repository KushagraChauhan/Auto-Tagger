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

bigram_measures = nltk.collocations.BigramAssocMeasures()

@app.route('/')


@app.route('/file-upload', methods=['POST'])
def file_upload():
    files = request.files.getlist("file")
    print(request.files)
    z = []
    for file in files:
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(filename))

        extension = os.path.splitext(filename)[1]
        print('extenion:',extension)
        if extension == ".pdf" or extension == ".docx":
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
                    z.append(json.loads(y))
            elif length>=5:
                for i in range(9):
                    print("Keywords:", key[i])
                    tags.append(key[i])
                    x = {"id":key[i],"text":key[i],"selected":"True"}
                    y = json.dumps(x)
                    z.append(json.loads(y))
        os.remove(os.path.join(filename))
    return jsonify({'data':z})

    # file_upload = request.files['file']
    # if file_upload:
    #     filename = secure_filename(file_upload.filename)
    #     file_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     extension = os.path.splitext(filename)[1]
    #     print('extenion:',extension)
    #
    #     if extension == ".pdf" or extension == ".docx":
    #         raw = parser.from_file(filename)
    #         r = Rake(max_length=2)
    #         text = raw['content']
    #         r.extract_keywords_from_text(text)
    #         key = r.get_ranked_phrases()
    #         print("test1---------")
    #         finder = BigramCollocationFinder.from_words(text)
    #         bigrm = list(nltk.bigrams(text.split()))
    #         print(*map(' '.join, bigrm), sep=', ')
    #         print("----------test2")
    #         # only bigrams that appear 3+ times
    #         #finder.apply_freq_filter(2)
    #         # return the 10 n-grams with the highest PMI
    #         grams = finder.nbest(bigram_measures.pmi, 5)
    #         print("grams",grams)
    #         tags = []
    #         length = len(key)
    #         z = []
    #         if length<5:
    #             for i in range(length):
    #                 print("Keywords:", key[i])
    #                 tags.append(key[i])
    #                 x = {"id":key[i],"text":key[i],"selected":"True"}
    #                 y = json.dumps(x)
    #                 z.append(json.loads(y))
    #         elif length>=5:
    #             for i in range(9):
    #                 print("Keywords:", key[i])
    #                 tags.append(key[i])
    #                 x = {"id":key[i],"text":key[i],"selected":"True"}
    #                 y = json.dumps(x)
    #                 z.append(json.loads(y))
    #         return jsonify({'data':z})

    # return "success"

if __name__ == "__main__":
    app.run(port=4500, debug=True)
