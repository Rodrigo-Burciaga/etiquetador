from flask import Blueprint, render_template, abort, request, url_for, redirect, flash, \
    send_file
from flask import current_app as app
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
import zipfile
import os

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'zip'}
file_handler = Blueprint('files', __name__,
                         template_folder='templates/files')


@file_handler.route('/', defaults={'page': 'index'}, methods=['POST', 'GET'])
@file_handler.route('/<page>', methods=['POST', 'GET'])
def file_index(page):
    if request.method == 'GET':
        try:
            return render_template('file.html')
        except TemplateNotFound:
            abort(404)
    else:
        return page


@file_handler.route('/upload_file', defaults={'page': 'index'}, methods=['POST'])
@file_handler.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(relative_file_name)
            unzip(relative_file_name, os.path.join(app.config['UPLOAD_FOLDER']))
            remove_zip(relative_file_name)
            return "guardado exitosamente"
        return render_template('error.html', error='Tu archivo no esta permitido')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@file_handler.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@file_handler.route('/show_files/<path>', defaults={'page': 'index'})
@file_handler.route('/show_files/<path>')
def show_files(path):
    try:
        list_files = os.listdir(os.path.join(app.static_folder, path))
        print(list_files)
        if not list_files:
            flash('No hay archivos en el directorio')
        return render_template("show_files.html", path=path, list_files=list_files)
    except FileNotFoundError as e:
        print('Archivo no encontrado')
        abort(404, description="Resource not found")


@file_handler.route('/download_file', methods=['POST'])
def download_file():
    if not request.form['file_name'] or not request.form['path']:
        return abort(400, description="No provided file name")
    try:
        return send_file(os.path.join(app.static_folder,
                                      request.form['path'], request.form['file_name']), as_attachment=True)
    except Exception:
        abort(404, description="Resource not found")


def unzip(relative_file_name, relative_current_path):
    with zipfile.ZipFile(relative_file_name, 'r') as zip_ref:
        zip_ref.extractall(relative_current_path)


def remove_zip(relative_file_name):
    os.remove(relative_file_name)
