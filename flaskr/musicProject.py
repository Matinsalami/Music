from flask import Flask, request, render_template, make_response, send_from_directory
import os
import threading

from helpers import upscaler, makePhoneLike , denoise_and_delay
app = Flask(__name__, static_folder="static",instance_relative_config=True)
_UPLOADED_ = 0
_FILE_NAME_ = ""
_CONFIGS_ = dict({})

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static")

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
        for k,v in _CONFIGS_.items():
            print (k)
            if k == "phone":
                makePhoneLike(int(v["phoneFilterOrder"]), int(v["phoneSideGain"]), _FILE_NAME_)
            if k == "upscale":
                upscaler(int(v["upscaleTargetWidth"]), int(v["upscaleTargetHeight"]), _FILE_NAME_)
            if k == "denoiseDelay":
                denoise_and_delay(_FILE_NAME_ , int (v["noisePower"]) , int(v["delay"]) , int(v["delayGain"]) )
        return render_template("project_template.html")
    
@app.route("/stream/", methods=["GET"])
def stream():
    return send_from_directory(UPLOAD_FOLDER,
                               "result.mp4", as_attachment=True)  
        