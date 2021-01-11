import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
from deepface import DeepFace

#Flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
bootstrap = Bootstrap(app)

class UploadForm(FlaskForm):
    upload = FileField('Select an image:', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'JPEG', 'PNG', 'JPG'], 'Images only!')
    ])
    submit = SubmitField('Classify')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.upload.data
        filename = secure_filename(f.filename)
        file_url = os.path.join('static', filename)
        f.save(file_url)
        form = None
        try:          
            obj = DeepFace.analyze(img_path = file_url, actions = [ 'gender', 'emotion'])
            prediction = [obj["dominant_emotion"], obj["gender"]]
        except ValueError:
            prediction = ["undefined"]
    else:
        file_url = None
        prediction = None
    return render_template("index.html", form=form, file_url=file_url, prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)


