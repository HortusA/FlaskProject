from flask import render_template, Blueprint, request
from wtforms import FileField, SubmitField, validators
from flask_wtf import FlaskForm


list_body = []
bp_file = Blueprint('write', __name__, template_folder='templates')
UPLOAD_FOLDER = ''


class UploadFileForm(FlaskForm):
    file = FileField("file", validators=(validators.InputRequired(),))
    submit = SubmitField("Чтение файла")


@bp_file.route('/upload', methods=['GET', "POST"])
def home():
    f = ReadFile('/home/alex/PycharmProjects/FlaskProject/syslog')
    page_num = 0 if request.args.get('page') is None else int(request.args.get('page'))
    if not page_num:
        return render_template('grossfile/index.html', data=f.current_page(page_num), page=1)
    else:
        return render_template('grossfile/index.html', data=f.current_page(page_num), page=page_num)


class ReadFile:

    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = None

    def read_text(self):
        form_read = open(self.file_path)
        self.lines = form_read.readlines()

    def current_page(self, page):
        if page == 1:
            return self.lines[0:20]
        else:
            return self.lines[20 * page:20 * page + 20]





