from flask import Flask, request, render_template, make_response

app = Flask(__name__)
_UPLOADED_ = 0
@app.route("/")
def hello_world():
    return render_template('project_template.html')


@app.route("/post/", methods=["POST"])
def uploadedVideo():
    global _UPLOADED_
    print(_UPLOADED_)
    if _UPLOADED_ == 1:
        mr = make_response(render_template("project_template.html"), 404)
        mr.headers["res"] = "You've already uploaded a file!"
        return mr
    else:
        print(request.files.get("file").filename)
        _UPLOADED_ = 1
    return render_template("project_template.html")



@app.route("/delete/", methods=["DELETE"])
def deletedVideo():
    global _UPLOADED_
    if _UPLOADED_ == 1:
        _UPLOADED_ = 0
        mr = make_response(render_template("project_template.html"), 204)
        mr.headers["res"] = "file deleted!"
        return mr



