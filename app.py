from flask import Flask, render_template, request, redirect, url_for, Response
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


# Route to serve the index page
@app.route('/hello/<username>')
def hello(username):
    # This renders the template that includes the image
    return render_template('hello.html', username=username, media_url="/image")


# Route to serve the image
@app.route('/image')
def image():
    # Presuming you have AWS credentials set up in your environment or using IAM roles in EC2
    s3 = boto3.client('s3')
    bucket_name = "rapkeb"
    image_file = "welcome.jpeg"

    # Get the image object from S3
    image_object = s3.get_object(Bucket=bucket_name, Key=image_file)

    # Serve the image as a response
    return Response(
        image_object['Body'].read(),
        mimetype='image/jpeg',
        headers={
            "Content-Disposition": "inline; filename={}".format(image_file)
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
