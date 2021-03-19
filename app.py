from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Post Class/Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.String(200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body')

# Init PostSchema
post_schema = PostSchema(strict=True)
posts_schema = PostSchema(many=True, strict=True)

# ROUTES

@app.route('/post', methods=['POST'])
def add_post():
    title = request.json['title']
    body = request.json['body']

    new_post = Post(title, body)

    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)

    

# Run Server
if __name__ == '__main__':
    app.run(debug=True)