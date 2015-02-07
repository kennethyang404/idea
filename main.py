from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/posts.db"

db = SQLAlchemy(app)

class posts(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    owner=db.column(db.String(100))
    title = db.Column(db.String(100))
    keywords=db.Column(db.String(100))
    objective = db.Column(db.String(1000))
    description=db.Column(db.String(1000))
    announcement=db.Column(db.String(1000))
    
    def __init__(self, owner, title, keywords,objective,description,announcement):
        self.owner=owner
        self.title=title
        self.keywords=keywords
        self.objective=objective
        self.description=description
        self.announcement=announcement

db.create_all()

#Helper Function Used by GRMmouse
def compare(left,right):
    return cmp(-left.score,-right.score)

def ownerHandler(owner):
    owner=owner[3:]
    if owner.split("%40")[1:]=="andrew.cmu.edu":
        owner=owner.split("%40")[0]
        return owner
    else:
        return None

def keywordsHandler(keywords):
    keywords=keywords[3:]
    if "," in keywords:
        return ";".join(keywords.split(","))
    elif ";" in keywords:
        return keywords
    else:
        return None

def contentHandler(content):
    "Takes the string after post/ and returns a posts object"
    content=(content[1:]).split("&")
    owner=ownerHandler(content[0])
    title=content[1][3:]
    keywords=keywordsHandler(content[2])
    objective=content[3][3:]
    description=content[4][3:]
    announcement=content[5][3:]
    if owner!=None and keywords!=None:
        return posts(owner,title,keywords,objective,description,announcement)
    else:
        return None


@app.route('/')
def login():
    return 'Login'

@app.route('/index')
def index():
    testttt="<p>Climb leg make muffins or sweet"
    test=[testttt]*4+(posts.query.all()[:1])*5
    return render_template("index.html", posts=test)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/newpost/<string:content>') 
def newpost(content):
    new=contentHandler(content)
    db.session.add(new)
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
