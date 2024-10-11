from flask import Flask, render_template, request, redirect
import os
from functions import process_video

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_heatmap', methods=['POST'])
def generate_heatmap():
    if 'videoFile' not in request.files:
        return redirect(request.url)
    video_file = request.files['videoFile']
    palette = request.form['palette']
    threshold = request.form['threshold']
    if video_file.filename == '':
        return redirect(request.url)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)
    process_video(video_path, palette, threshold)
    return render_template('index.html', heatmap_image='static/heatmap.png')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
