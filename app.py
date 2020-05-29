import argparse
import datetime
from flask import Flask, render_template, request, send_from_directory
import glob
import json
import os
import time
import threading
from videofile import VideoFile

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
    help="path to the JSON configuration file")
args = vars(ap.parse_args())
conf = json.load(open(args["conf"]))
videoDir = conf["video_dir"];

def reverseLettersInWords(text):
    reversedText = ''
    words = text.split()
    for word in words:
        reversedWord = word[::-1]
        reversedText += reversedWord + ' '
    
    return reversedText

def sanitiseFilename(filename):
    return os.path.basename(os.path.realpath(filename))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

@app.route('/hello')
def helloFromForm():
    name = request.args.get('name')
    return hello(name)

@app.route('/secret')
def secret():
    text = request.args.get('text')
    secretText = reverseLettersInWords(text)
    return render_template('secret.html', text=text, secretText=secretText)

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/more-activities')
def moreActivities():
    return render_template('more-activities.html')

@app.route('/more-recipes')
def moreRecipes():
    return render_template('more-recipes.html')

@app.route('/useful-links')
def usefulLinks():
    return render_template('useful-links.html')

@app.route('/dinosaurs')
def dinosaurs():
    return render_template('dinosaurs.html')

@app.route('/cattracker')
def cattracker():
    fromDateTime = datetime.datetime.now() - datetime.timedelta(days=1)
    videos = filter (
        lambda x: x.timestamp >= fromDateTime,
        sorted(
            map(VideoFile, glob.glob(os.path.join(videoDir, "*.mp4"))),
            key=lambda x: x.timestamp, reverse=True)
        );
    return render_template('cattracker2000.html', videos=videos)

@app.route('/cattracker/videos')
def cattrackerVideo():
    filename = sanitiseFilename(request.args.get('filename'))
    videoFile = VideoFile(os.path.join(videoDir, filename))
    return render_template('cattracker-video.html', filename=filename, timestamp=videoFile.displayName)

@app.route('/cattracker/videos/<filename>')
def cattrackerVideoFile(filename):
    filename = sanitiseFilename(filename)
    return send_from_directory(videoDir, filename)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int('80'))
