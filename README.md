## Auto-Tagger

***This repo will help to get the tags from a file.***
Install all the required modules by-
		
		pip3 install -r requirements.txt
		
---
How to run the file-

		python3 main_app.py

After that open:
	
		http://localhost:4500/file-upload

and upload the files.

---

3 main files-
--app.py
--main.py
--main_app.py
And their functions-
1.  Download the file using URL and give the response
2.  Work on the server as a system API and store the tags in a DB 
3.  Work in-sync with KM, and give real-time response
---
Keyword extraction technique used-
### RAKE-
Rapid Automatic Keyword Extraction (RAKE) is a well-known keyword extraction method which uses a list of stopwords and phrase delimiters to detect the most relevant words or phrases in a piece of text.

---
Parser used to parse the text from a pdf or a docx-
### TIKA-
Tika works on .pdf, the most recent OOXML Microsoft Office file types and older binary file formats such as .doc, .ppt and .xls.

---



