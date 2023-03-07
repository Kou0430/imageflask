from google.cloud import vision
import os
from flask import Flask, render_template, request


# 認証情報取得
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "premium-aurora-379604-741bde1aeb70.json"

# Vision APIクライアントを作成
client = vision.ImageAnnotatorClient()

app = Flask(__name__)

IMG_URL = "https://t3.ftcdn.net/jpg/01/43/83/08/240_F_143830808_V7n31HxcS8duJIVr3opWzG4FCkDQZK4v.jpg"


@app.route("/", methods=["GET", "POST"])
def picture():
    if request.method == "POST":

        if not request.form.get("picture"):
            image = vision.Image()
            image.source.image_uri = IMG_URL
            print("get!")
            print(image.source.image_uri)
            return render_template("index.html")

        if request.form.get("picture"):

            image = vision.Image()
            image.source.image_uri = request.form.get("picture")

            response = client.label_detection(image=image)
            labels = response.label_annotations

            for label in labels:
                print(label.description + ":" + str(label.score))

            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
            return render_template("index.html")

    else:
        return render_template("index.html")

