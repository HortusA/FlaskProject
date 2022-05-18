from flask import Flask, render_template, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

app = Flask(__name__, template_folder='/home/alex/PycharmProjects/FlaskProject/templates/user_login/')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = 'secret'
app.config['EXPLAIN_TEMPLATE_LOADING'] = True


db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = '/login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    pass_hash = db.Column(db.String(100))

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegFormUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repid', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Добавить')

    def valid_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('измените имя.')

    def valid_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('такой емайл есть')


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'неправельный логин или пароль')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        return redirect('index')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegFormUser()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        #db.session.commit()
        flash(u'Пользователь зарегестрирован!')
        return redirect('login')
    return render_template('register.html', form=form)


app.run(debug=True)
