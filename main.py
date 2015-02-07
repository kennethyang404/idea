from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/projects.db"

db = SQLAlchemy(app)

class projects(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ownerr=db.Column(db.String(100))
    title = db.Column(db.String(100))
    keywords=db.Column(db.String(100))
    objective = db.Column(db.String(1000))
    description=db.Column(db.String(1000))
    requirement=db.Column(db.String(1000))
    announcement=db.Column(db.String(1000))
    
    def __init__(self, ownerr, title, keywords,objective,description,requirement,announcement):
        self.ownerr=ownerr
        self.title=title
        self.keywords=keywords
        self.objective=objective
        self.description=description
        self.requirement=requirement
        self.announcement=announcement

db.create_all()

#Helper Function Used by GRMmouse

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
    owner=content["q1"]
    title=content["q2"]
    keywords=keywordsHandler(content["q3"])
    objective=content["q4"]
    description=content["q5"]
    requirement=content["q6"]
    announcement=content["q7"]
    #if keywords!=None:
    return projects(owner,title,content["q3"],objective,description,requirement,announcement)
    #else:
    #    return None


@app.route('/')
def login():
    return 'Login'

@app.route('/index')
def index():
    test=(projects.query.all()[:4])*3
    return render_template("index.html", posts=test)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/newpost', methods=["POST"]) 
def newpost():
    newProject=contentHandler(request.form)
    db.session.add(newProject)
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
