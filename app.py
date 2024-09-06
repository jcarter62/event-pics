from flask import Flask, render_template, send_from_directory, send_file
from images import Loader

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

if __name__ == '__main__':
    app.run()
