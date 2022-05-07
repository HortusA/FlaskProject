import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main import app
from sqlalchemy.dialects.mysql import TINYINT, INTEGER


basedir = os.path.abspath(os.path.dirname(__file__))


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app_sql.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TableModels(db.Model):
    id = db.Column(INTEGER(unsigned=True), index=True)
    invoice = db.Column(INTEGER(unsigned=True), index=True, default='0')
    time = db.Column(db.DateTime, index=True, default='1970-01-01 00:00:00')
    amount = db.Column(INTEGER(unsigned=True), index=True, default='0')
    text = db.Column(db.Text)
    ourid = db.Column(INTEGER(unsigned=True), index=True, default='0')
    type = db.Column(db.VARCHAR(100))
    username = db.Column(db.VARCHAR(500))
    service = db.Column(db.Text)
    source = db.Column(db.VARCHAR(100))
    op_userid = db.Column(db.VARCHAR(500))
    op_source = db.Column(db.VARCHAR(500))
    op_campaign = db.Column(db.VARCHAR(500))
    op_medium = db.Column(db.VARCHAR(500))
    op_target = db.Column(db.VARCHAR(500))
    op_term = db.Column(db.VARCHAR(500))
    op_campaignid = db.Column(db.VARCHAR(500))
    op_adgroupid = db.Column(db.VARCHAR(500))
    op_adid = db.Column(db.VARCHAR(500))
    op_nwletter = db.Column(db.VARCHAR(500))
    op_devtype = db.Column(db.VARCHAR(500))
    op_refpartner = db.Column(db.VARCHAR(500))
    op_yamid = db.Column(db.VARCHAR(500))
    cqflag = db.Column(TINYINT(unsigned=True),default='0')
    pwflag = db.Column(TINYINT(unsigned=True),default='0')
    yamflag = db.Column(TINYINT(unsigned=True),default='0')




