import os
from openpyxl import load_workbook
import sqlite3
from flask import render_template, Blueprint
from wtforms import FileField, SubmitField, DateField, validators
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm


path_to_base = '/media/i7_nfs/storage/develop/python/FlaskProject/app.sqlite'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()


list_body = []
bp_nris = Blueprint('nris', __name__, template_folder='templates')
UPLOAD_FOLDER = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("file")
    start = DateField("start", format='%Y-%m-%d', validators=(validators.Optional(),))
    end = DateField("end", format='%Y-%m-%d', validators=(validators.Optional(),))
    submit = SubmitField("Загрузка файла")


@bp_nris.route('/upload', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        start_data = form.start.data
        end_data = form.end.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_FOLDER,
                                 secure_filename(file.filename))
        file.save(file_path)
        d = EmailList(file_path)
        res = d.list_pyxl(start_data,end_data)

        return render_template('/nris/index.html', form=form, data=res)
    return render_template('/nris/index.html', form=form)


class EmailList:       # работа с файлом xls для задачи2
    def __init__(self, file_path):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.file_path = file_path

    def list_pyxl(self, data_start, data_end):
        self.data_start = data_start
        self.data_end = data_end
        new_xls_email_list = []
        wb = load_workbook(self.file_path)
        for sheet in wb.worksheets:
            if sheet.sheet_state == 'visible':
                column = sheet["A"]
                for one_email in range(len(column)):
                    data_email = str(column[one_email].value)
                    if '@' in data_email:
                        new_xls_email_list.append(data_email)
        print(self.data_end)

        sql = "','".join(new_xls_email_list)
        self.cursor.execute(f"""SELECT
                                    username, sum(amount) as sum
                                    FROM f_lk_payments
                                    WHERE username in ('{sql}')
                                    and time > ('{self.data_start}') and time < ('{self.data_end}')
                                    group by username
                                    """)
        res = self.cursor.fetchall()
        return res