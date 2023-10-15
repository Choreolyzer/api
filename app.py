import os
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil


app = Flask(__name__)
CORS(app)


# util functions
def is_valid_video(file):
    return "mp4" in file.filename


def cleanup():
    shutil.rmtree("assets/")
    os.mkdir("assets")
    os.mkdir("assets/mot")
    os.mkdir("assets/mot/dances")
    os.mkdir("assets/mot/dances/img1")
    return


@app.route("/upload", methods=["POST"])
def upload():
    video = request.files['file']
    points = request.form['points']
    print(points)
    if video:
        if is_valid_video(video):
            video.save(os.path.join("assets/", "video.mp4"), buffer_size=None)

            # create YOLOX det_db

            # apply MOTORv2

            # run viz script
            # viz.create_visualized()     # assets/out.avi

            # modifies transforms

            # send transforms back to user

            # cleanup
            os.system("source ./run.sh")


            return "Video uploaded successfully."
        else:
            return "Invalid video format"
    return "Invalid video format or no file found."


@app.route("/poll", methods=["GET"])
def poll():
    if "out.avi" in os.listdir("assets"):
        with open("asset/out.avi", 'rb') as f:
            video_data = f.read()

        video_data = base64.b64encode(video_data).decode('utf-8')
        data = {
                "video": video_data,
                "transforms": {}
                }
        return jsonify(data)
    return "loading"
