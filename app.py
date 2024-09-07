from flask import Flask, render_template, send_from_directory, send_file, redirect, request, url_for
from images import Loader
import os
from waitress import serve # for production

app = Flask(__name__)


@app.route('/')
def root_path():  # put application's code here
    l = Loader()
    context = {'files': l.get_files()}
    return render_template('home.html', **context)


@app.route('/pics/<filename>')
def get_pic(filename):
    l = Loader()
    file_info = l.get_file_info(filename)
    text = l.file_text.get(file_info['file'], '')
    return render_template('one-picture.html', file_info=file_info, text=text)

@app.route('/static/pics/<filename>')
def get_static_pic(filename):
    return send_from_directory('static/pics', filename), 200

@app.route('/static/<filename>')
def get_static_filename(filename):
    return send_from_directory('static', filename), 200


@app.route('/pics/<filename>/delete')
def delete_pic(filename):
    l = Loader()
    l.delete_file(filename)
    return redirect('/')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            file.save(os.path.join(os.getenv('PICTURE_PATH',''), filename))
            return redirect(url_for('root_path'))
    return render_template('upload.html')

@app.route('/pics/<file>/text', methods=['GET', 'POST'])
def add_text(file):
    if request.method == 'POST':
        filename = request.form['filename']
        text = request.form['text']
        text_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(os.getenv('PICTURE_PATH', ''), text_filename), 'w') as text_file:
            text_file.write(text)
        return redirect(url_for('root_path'))
    else:
        l = Loader()
        file_info = l.get_file_info(file)
        orig_text = l.file_text.get(file_info['file'], '')
        return render_template('add-text.html', filename=file, orig_text=orig_text)

# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)
