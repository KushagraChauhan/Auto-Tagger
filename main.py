from tika import parser
from rake_nltk import Rake,  Metric
import json, threading
from flask import Flask, request, jsonify, render_template,session,jsonify
from flask_apscheduler import APScheduler
import mysql.connector
import os

app = Flask(__name__)
@app.route('/auto-tagger' ,methods=['POST','GET'])
def thp():

    db = mysql.connector.connect(
    db_host=os.getenv("HOST"),
    db_user=os.getenv("USER"),
    db_password=os.getenv("PASSWORD"),
    db_database=os.getenv("DATABASE")
    #db_port=os.getenv("PORT")
    )
    cursor = db.cursor(buffered=True)
    cursor_fin = db.cursor(buffered=True)
    #cursor = conn.cursor()
    # file_location_query = ("SELECT filemanager_filepath FROM `file_tag_managers` WHERE `status`=`unprocessed`")
    file_location_query = ("SELECT filemanager_filepath FROM `file_tag_managers`")
    cursor.execute(file_location_query)
    for j in cursor:
        print(j)
        file_path = '/opt/lamp/apps/test/storage/app/file-manager/' + j[0]
        print(file_path)
#raw = parser.from_file(cursor)
#raw = parser.from_file('/home/kush/lamp/apps/forebase/storage/app/file-manager/files/shares/1.docx')
        file_len = len()
        path = urlparse(file_path).path
        ext = splitext(path)[1]
        if ext == ".pdf" or ext == ".docx":
            raw = parser.from_file(file_path)
            r = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=1)
            text = raw['content']
            r.extract_keywords_from_text(text)
            key = r.get_ranked_phrases()
            tags = []
            length = len(key)
            if length<5:
                for i in range(length):
                    print("Keywords:", key[i])
                    tags.append({"en":key[i]})
                    sql = "INSERT INTO tags (name, slug) VALUES (%s, %s)"
                    val = (json.dumps(tags[i]),json.dumps(tags[i]))
                    cursor_fin.execute(sql, val)

            elif length>=5:
                for i in range(3):
                    print("Keywords:", key[i])
                    tags.append({"en":key[i]})
                    sql = "INSERT INTO tags (name, slug) VALUES (%s, %s)"
                    val = (json.dumps(tags[i]),json.dumps(tags[i]))
                    cursor_fin.execute(sql, val)

        continue
        db.commit()

    return "success"
#
# def mit():
#     db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123456",
#     database="test"
#     )
#     cursor = db.cursor()
#     # file_location_query = ("SELECT filemanager_filepath FROM `file_tag_managers` WHERE `status`=`unprocessed`")
#     file_location_query = ("SELECT filemanager_filepath FROM `file_tag_managers`")
#     cursor.execute(file_location_query)
#     for i in cursor:
#         print(i)
# #    raw = parser.from_file(cursor)
#
#     raw = parser.from_file('/home/kush/lamp/apps/forebase/storage/app/file-manager/files/shares/1.docx')
#     r = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=1)
#     text = raw['content']
#     r.extract_keywords_from_text(text)
#     key = r.get_ranked_phrases()
#     tags = []
#     length = len(key)
#     if length<5:
#         for i in range(length):
#             print("Keywords:", key[i])
#             tags.append(key[i])
#     elif length>=5:
#         for i in range(3):
#             print("Keywords:", key[i])
#             tags.append(key[i])
#
#     sql = "INSERT INTO tag (file_name, tags, status) VALUES (%s, %s, %s)"
#     val = ("file_name", json.dumps(tags), "processed")
#     cursor.execute(sql, val)
#     db.commit()
#     return "success"
#
# threading.Thread(target=thp).start()
# threading.Thread(target=mit).start()

if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.add_job(func=thp, trigger='interval', id='job', seconds=60)
    scheduler.start()
    app.run(port=4500, debug=True)
