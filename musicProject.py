from flask import Flask, request, render_template, make_response
import os
import threading
import ffmpeg
from helpers import fileSaver
app = Flask(__name__)
_UPLOADED_ = 0
_FILE_NAME_ = ""
_CONFIGS_ = dict({})

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
        request.files["file"].save(request.files["file"].filename)
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

@app.route("/configurefilter/", methods=["POST"])
def saveConfiguration():
    global _CONFIGS_
    _CONFIGS_.clear()
    for l in request.get_json():
        _CONFIGS_[l["name"]] = {v["name"]: v["value"] for v in l["props"]} ## For easier use! 
    return render_template('project_template.html')
    

@app.route("/applyfilter/", methods=["GET"])
def applyFilter():
    global _CONFIGS_, _FILE_NAME_
    if not _CONFIGS_ or not _FILE_NAME_:
        mr = make_response(render_template("project_template.html"), 403)
        mr.headers["res"] = "Missing file or config!"
        return mr   
    else:
        return render_template("project_template.html")
    
        
