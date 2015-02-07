from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/posts.db"

db = SQLAlchemy(app)

class posts(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    subtitle=db.Column(db.String(140))
    text = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    
    def __init__(self, title, subtitle, text, score):
        self.title = title
        self.subtitle=subtitle
        self.text = text
        self.score=score
        self.date = datetime.utcnow()

db.create_all()


#Helper Function Used by GRMmouse
def compare(left,right):
    return cmp(-left.score,-right.score)

def createTitle(text):
    if (text != None) and (len(text) <= 140):
        return text
    else:
        return None

def createNewText(text):
    if (text!=None) and (len(text)<=1000):
        return text
    else:
        return None


@app.route('/')
def login():
    return 'Login'

@app.route('/index')
def index():
    posts=sorted(db.query.all(),compare)[0:9]
    return render_template("index.html",posts=posts)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/newpost/<string:content>')
def newpost(content):
    newTitle="content"
    newSubtitle="Cde"
    newText="efg"
    newScore=20
    db.session.add(posts(newTitle,newSubtitle,newTitle,newScore))
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return "about.html"

@app.route("/usr/<int:user_id>")
def user(user_id):
    return "User: %d" %user_id

if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0')
