from flask import Flask, flash, render_template, request, redirect, url_for, make_response, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy import SQLAlchemy
from wtforms import SubmitField, TextAreaField
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import secrets
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Daha güvenli bir secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max-size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Veritabanı modellerini güncelle
class Thought(db.Model):
    __tablename__ = 'thought'
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20))
    day = db.Column(db.Integer)
    content = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProfileForm(FlaskForm):
    photo = FileField('Profile Photo', 
                     validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Upload')

class ThoughtForm(FlaskForm):
    content = TextAreaField('My Thoughts')
    photo = FileField('Add Image', 
                     validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Save')

def get_first_day_of_month(month_num):
    first_day = calendar.monthcalendar(datetime.now().year, month_num)[0]
    for i, day in enumerate(first_day):
        if day != 0:
            return i
    return 0

def init_db():
    with app.app_context():
        db.create_all()
        if not Profile.query.first():
            default_profile = Profile()
            db.session.add(default_profile)
            db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_file(file, folder_name=""):
    if file and allowed_file(file.filename):
        # Benzersiz dosya adı oluştur
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
        
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        filepath = os.path.join(folder_path, unique_filename)
        file.save(filepath)
        return filepath
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    profile_form = ProfileForm()
    thought_form = ThoughtForm()

    # Ayları ve günleri tanımla
    months = {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December"
    }
    
    month_days = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    # Profil fotoğrafı işlemleri
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        if file.filename != '':
            filepath = save_file(file, 'profiles')
            if filepath:
                profile = Profile.query.first() or Profile()
                if profile.image_path:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], profile.image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                profile.image_path = filepath
                db.session.add(profile)
                db.session.commit()
                flash('Profile photo updated successfully!', 'success')
                return redirect(url_for('index'))

    profile = Profile.query.first()
    thoughts = Thought.query.all()
    
    entries = {}
    for thought in thoughts:
        entries[f"{thought.month}-{thought.day}"] = {
            'content': thought.content,
            'image': thought.image_path,
            'updated_at': thought.updated_at
        }

    return render_template('index.html',
                         profile_form=profile_form,
                         thought_form=thought_form,
                         profile_image=profile.image_path if profile else None,
                         months=months,
                         month_days=month_days,
                         entries=entries,
                         get_first_day_of_month=get_first_day_of_month)

@app.route('/thoughts/<month>/<day>', methods=['GET', 'POST'])
def thoughts(month, day):
    form = ThoughtForm()
    thought = Thought.query.filter_by(month=month, day=day).first()

    if form.validate_on_submit():
        if not thought:
            thought = Thought(month=month, day=day)
        
        thought.content = form.content.data

        if form.photo.data:
            filepath = save_file(form.photo.data, f'thoughts/{month}')
            if filepath:
                # Eski fotoğrafı sil
                if thought.image_path and os.path.exists(thought.image_path):
                    os.remove(thought.image_path)
                thought.image_path = filepath

        db.session.add(thought)
        db.session.commit()
        flash('Your thought has been saved!', 'success')
        return redirect(url_for('index'))

    if thought:
        form.content.data = thought.content

    return render_template(
        'thoughts.html',
        thought_form=form,
        month=month,
        day=day,
        thought=thought
    )

@app.route('/remove_profile_photo', methods=['POST'])
def remove_profile_photo():
    profile = Profile.query.first()
    if profile and profile.image_path:
        if os.path.exists(profile.image_path):
            os.remove(profile.image_path)
        profile.image_path = None
        db.session.commit()
        flash('Profile photo removed successfully!', 'success')
    return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)





