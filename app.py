import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    regdate = db.Column(db.DateTime,default=datetime.now())

with app.app_context():
    db.create_all()

@app.route('/',methods=['GET'])
def index():
    user_list = User.query.order_by(User.score.desc())
    return render_template('index.html',user_list=user_list)

@app.route('/',methods=['POST'])
def post():
    name = request.args.get('name')
    score = request.args.get('score')
    user = User(name=name,score=score)
    db.session.add(user)
    db.session.commit()
    return '처리 완료'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)