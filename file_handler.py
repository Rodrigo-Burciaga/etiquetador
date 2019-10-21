import logging
import os
import zipfile

from flask import Blueprint, render_template, abort, request, flash, \
    send_file
from flask import current_app as app
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'zip', 'rar', '7z'}
file_handler = Blueprint('files', __name__,
                         template_folder='templates/files')


@file_handler.route('/file', methods=['GET'])
def file_index():
    return render_template('file.html')


@file_handler.route('/upload_file', methods=['POST'])
@file_handler.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No se pudo obtener el archivo'
    file = request.files['file']
    if file.filename == '':
        return 'no seleccionaste ningún archivo'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        relative_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(relative_file_name)
        try:
            unzip(relative_file_name, os.path.join(app.config['UPLOAD_FOLDER']))
        except Exception as e:
            return str(e)

        delete_zip(relative_file_name)
        return "guardado exitosamente"
    return 'Tu archivo no esta permitido'


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
        logging.info(list_files)
        if not list_files:
            flash('No hay archivos en el directorio')

        return render_template("show_files.html", path=path, list_files=list_files)
    except FileNotFoundError as e:
        logging.warn('Archivo no encontrado' + str(e))
        abort(404, description="Resource not found")


@file_handler.route('/download_file', methods=['POST'])
def download_file():
    if not request.form['file_name'] or not request.form['path']:
        return abort(400, description="No provided file name")
    try:
        return send_file(os.path.join(app.static_folder,
                                      request.form['path'], request.form['file_name']), as_attachment=True)
    except Exception as e:
        abort(404, description="Resource not found" + str(e))


def unzip(relative_file_name, relative_current_path):
    try:
        with zipfile.ZipFile(relative_file_name, 'r') as zip_ref:
            zip_ref.extractall(relative_current_path)
    except Exception as e:
        logging.error(e)
        raise Exception('No es un archivo zip')


def delete_zip(relative_file_name):
    os.remove(relative_file_name)
