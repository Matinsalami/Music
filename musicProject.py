from flask import Flask, request, render_template, make_response
import os
import threading
from helpers import fileSaver
app = Flask(__name__)
_UPLOADED_ = 0
_FILE_NAME_ = ""

@app.route("/")
def hello_world():
    return render_template('project_template.html')


@app.route("/post/", methods=["POST"])
def uploadedVideo():
    global _UPLOADED_, _FILE_NAME_
    if _UPLOADED_ == 1:
        mr = make_response(render_template("project_template.html"), 404)
        mr.headers["res"] = "You've already uploaded a file!"
        return mr
    else:
        threading.Thread(target=fileSaver, args=(request.files["file"], )).start()
        _UPLOADED_ = 1
        _FILE_NAME_ = request.files["file"].filename
    return render_template("project_template.html")



@app.route("/delete/", methods=["DELETE"])
def deletedVideo():
    global _UPLOADED_, _FILE_NAME_
    if _UPLOADED_ == 1:
        _UPLOADED_ = 0
        os.remove(_FILE_NAME_)
        _FILE_NAME_ = ""        
        mr = make_response(render_template("project_template.html"), 204)
        mr.headers["res"] = "file deleted!"
        return mr
    else: 
        return render_template('project_template.html')



