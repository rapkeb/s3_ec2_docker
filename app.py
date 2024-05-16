from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import boto3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)


# Create the database
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('hello', username=username))
        except:
            return 'There was an issue adding your details'
    return render_template('index.html')


@app.route('/hello/<username>')
def hello(username):
    s3 = boto3.client('s3')
    bucket_name = 'rapkeb'
    media_url = f'https://{bucket_name}.s3.amazonaws.com/welcome.jpeg'
    return render_template('hello.html', username=username, media_url=media_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
