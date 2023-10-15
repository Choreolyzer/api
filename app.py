import os
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
from subprocess import Popen
import cv2
import numpy as np


app = Flask(__name__,
            static_url_path='', 
            static_folder='assets/'
            )

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


def transform_point(point, M):
    """
    Transforms a point using the given transformation matrix M.

    Parameters:
        point (tuple): The (x, y) coordinates of the point.
        M (numpy.array): The transformation matrix.

    Returns:
        (numpy.array): The transformed point.
    """
    src = np.array([[point]], dtype=np.float32)
    dst = cv2.perspectiveTransform(src, M)
    return dst[0,0]


colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (100, 100, 100),
    (255, 255, 255),
    ]

def create_video(data):
    print('trying to create video')
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    out = cv2.VideoWriter('assets/birdeye.webm', fourcc, 30.0, (1920, 1080))

    for frame_info in data:
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        for ID, x, y in data[frame_info]:
            cv2.circle(frame, (int(x), int(y)), 12, colors[int(ID) % 7], -1)
        # cv2.imshow('frame', frame)
        #
        # key = cv2.waitKey(1)
        # if key == ord('q'):
        #     break
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()

def process_birds_eye(transformation_matrix):
    print('processing bird eye')
    data = {}
    with open('assets/out.txt', 'r') as file:
        for line in file.readlines():
            frame_number, ID, x1, y1, width, height, t1, t2, t3, t4 = line.split(',')
            # print(f"ID: {ID}, Frame: {frame_number}, x1: {x1}, y1: {y1}, Width: {width}, Height: {height}")
            point_x = (float(x1) + float(width)/2)
            point_y = float(y1) + float(height)
            transform = transform_point((point_x, point_y), transformation_matrix)
            if not frame_number in data:
                data[frame_number] = []
            data[frame_number].append((ID, transform[0], transform[1]))
    create_video(data)


desired_points = np.float32([[0, 1080], [0, 0], [1920, 0], [1920, 1080]])    # Replace with desired coordinates


@app.route("/upload", methods=["POST"])
def upload():
    video = request.files['file']
    points = request.form['points']
    print(points)

    if video:
        if is_valid_video(video):
            # get video width and height
            video.save(os.path.join("assets/", "video.mp4"), buffer_size=None)

            # create YOLOX det_db

            # apply MOTORv2

            # run viz script
            # viz.create_visualized()     # assets/out.avi

            # modifies transforms

            # send transforms back to user

            # cleanup
            foo = Popen("source ./run.sh", shell=True, executable="/bin/bash")
            foo.wait();

            x1, y1, x2, y2, x3, y3, x4, y4 = points.split(',')
            x1, y1, x2, y2, x3, y3, x4, y4 = float(x1), float(y1), float(x2), float(y2), float(x3), float(y3), float(x4), float(y4)
            original_points = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

            transformation_matrix = cv2.getPerspectiveTransform(original_points, desired_points)
            process_birds_eye(transformation_matrix)

            return "Video uploaded successfully."
        else:
            return "Invalid video format"
    return "Invalid video format or no file found."


@app.route("/poll", methods=["GET"])
def poll():
    if "out.webm" in os.listdir("assets"):
        return "finished"
    return "loading"
