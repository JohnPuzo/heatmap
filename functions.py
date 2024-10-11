import os
import shutil
import subprocess
import cv2
import numpy as np

def clear_folder():
    if os.path.exists('frames'):
        shutil.rmtree('frames')

def delete_file():
    if os.path.exists('static/heatmap.png'):
        os.remove('static/heatmap.png')

def extract_motion_frames(input_video, threshold):
    if not os.path.exists("frames"):
        os.makedirs("frames")
    command = ['ffmpeg', '-i', input_video, '-vf', f'select=gt(scene\,{threshold})', '-fps_mode', 'vfr',
               os.path.join('frames', 'frame_%03d.png')]
    subprocess.run(command)


def create_heatmap(color_map):
    changes = []
    frames = sorted([os.path.join('frames', f) for f in os.listdir('frames')])
    for i in range(len(frames) - 1):
        img1 = cv2.imread(frames[i])
        img2 = cv2.imread(frames[i + 1])
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        changes.append(thresh)
    color_maps = {'viridis': cv2.COLORMAP_VIRIDIS, 'plasma': cv2.COLORMAP_PLASMA, 'inferno': cv2.COLORMAP_INFERNO,
                  'magma': cv2.COLORMAP_MAGMA, 'cividis': cv2.COLORMAP_CIVIDIS}
    colormap_code = color_maps[color_map]
    heatmap = np.sum(changes, axis=0).astype(np.uint8)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_colored = cv2.applyColorMap(heatmap, colormap_code)
    cv2.imwrite('static/heatmap.png', heatmap_colored)


def process_video(video_path, palette, threshold):
    clear_folder()
    delete_file()
    extract_motion_frames(video_path, threshold)
    create_heatmap(palette)
