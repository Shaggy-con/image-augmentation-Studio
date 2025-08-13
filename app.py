# app.py
from flask import Flask, request, send_file, render_template
import tempfile
import os
from augmentation import augment_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/augment', methods=['POST'])
def augment():
    image_file = request.files['image']
    params = request.form

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_in:
        image_file.save(temp_in)
        input_path = temp_in.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_out:
        output_path = temp_out.name

    augment_image(
        image_path=input_path,
        output_path=output_path,
        rotation=int(params.get('rotation', 0)),
        scale=float(params.get('scale', 1.0)),
        flip_horizontal=params.get('flip_horizontal') == 'on',
        flip_vertical=params.get('flip_vertical') == 'on',
        brightness=float(params.get('brightness', 1.0)),
        contrast=float(params.get('contrast', 1.0)),
        saturation=float(params.get('saturation', 1.0)),
        grayscale=params.get('grayscale') == 'on'
    )

    os.remove(input_path)
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)