from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages  
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from time import time



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Projects.db"
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

class Projects(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    owner=db.Column(db.String(255))
    title = db.Column(db.String(255))
    keywords=db.Column(db.String(255))
    objective = db.Column(db.String(1000))
    description=db.Column(db.String(1000))
    requirement=db.Column(db.String(1000))
    announcement=db.Column(db.String(1000))
    score = db.Column(db.Integer)
    date = db.Column(db.Integer)
    
    def __init__(self, owner, title, keywords, objective, description, requirement, announcement):
        self.owner=owner
        self.title=title
        self.keywords=keywords
        self.objective=objective
        self.description=description
        self.requirement=requirement
        self.announcement=announcement
        self.score=3
        self.date=int(time())


class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    follow = db.Column(db.Integer)
    post = db.Column(db.Integer)

    def __init__(self, name, password, follow=0, post=0):
        self.name = name
        self.password = password
        self.follow = follow
        self.post = post
    
    @classmethod
    def verify(self, name, password):
        expect = User.query.filter_by(name=name).first()
        if (expect==None)or(expect.password != password):
            return False
        else:
            return expect

    def is_authenticated(self):
        return (User.verify(self.name,self.password) != False)

    def is_active(self):
        return self.is_authenticated()

    def is_anonymous(self):
        return not self.is_authenticated()

    def get_id(self):
        return self.ID

    @classmethod
    def get(self_class, id):
        try:
            return User.query.filter_by(ID=id).first()
        except UserNotFoundError:
            return None

    @classmethod
    def used(self_class, name):
        return (User.query.filter_by(name=name).first() != None)

    @classmethod
    def add(self_class, name, password):
        user=User(name, password)
        db.session.add(user)
        db.session.commit()
        return user

db.create_all()



@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        form = request.form
        user=User.verify(form["email"],form["password"])
        if (user != False):
            login_user(user)
            flash("Logged in successfully.")
            print "!!!!!!!"
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup():
    form = request.form
    print User.used(form["email"])
    if (not User.used(form["email"])) and (form["password"]==form["confirm"]):
        user=User.add(form["email"], form["password"])
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("index"))
    return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def ownerHandler(owner):
    if owner.endswith("cmu.edu"):
        return owner.split("@")[0]
    return None

def keywordsHandler(keywords):
    return keywords.replace(",",";")

def contentHandler(content):
    "Takes the string after post/ and returns a posts object"
    owner=ownerHandler(content["q1"])
    title=content["q2"]
    keywords=keywordsHandler(content["q3"])
    objective=content["q4"]
    description=content["q5"]
    requirement=content["q6"]
    announcement=content["q7"]
    if owner:
        return Projects(owner,title,content["q3"],objective,description,requirement,announcement)
    else:
        return None

def searchHandler(content):
    keywords=content.split(" ")
    return [keywords[i] for i in xrange(len(keywords)) if keywords[i]!=""]

def wordSearch(word,item):
    return (word in item.description.lower()) or (word in item.requirement.lower()) or (word in item.keywords.lower()) or (word in item.objective.lower()) or (word in item.owner.lower()) or (word in item.announcement.lower()) or (word in item.title.lower())

def compareScore(left,right):
    return cmp(-left.score,-right.score)

def compareDate(left,right):
    return cmp(-left.date,-right.date)

@app.route('/')
@app.route('/index')
@login_required
def index():
    post=Projects.query.order_by(Projects.score).limit(9).all()
    #post on the main page, recent for the search box
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html", posts=post,recents=recent)

#These two below are for creating new Projects
@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/newpost', methods=["POST"]) 
def newpost():
    newProject=contentHandler(request.form)
    if newProject:
        db.session.add(newProject)
        db.session.commit()
    return redirect(url_for("index"))

@app.route('/search', methods=["POST"])
def search():
    content=request.form["searchbox"]
    keywords=searchHandler(content)
    result=list()
    for word in keywords:
        for item in Projects.query.all():
            if wordSearch(word.lower(),item):
                result.append(item)
    result=sorted((sorted(result,compareDate)[:15]),compareScore)[:9]
    for item in result:
        item.score+=1
        db.session.commit()
        
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html",posts=result,recents=recent)

@app.route('/detail/<int:ID>')
def detail(ID):
    result=[Projects.query.get(ID)]
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html",posts=result,recents=recent)

@app.route("/about")
def about():
    return "about.html"

@app.route("/usr/<int:user_id>")
def user(user_id):
    return "User: %d" %user_id

if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0')
