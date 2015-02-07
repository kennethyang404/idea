from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required, user_logged_in
from flask_oauth import OAuth
from time import time



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Projects.db"
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

# Facebook Login
app.config['FACEBOOK_APP_ID'] = '1540336042908904'
app.config['FACEBOOK_APP_SECRET'] = '036bb9bb8937f6499e3c6ddc8634cbfc'
oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'})

db = SQLAlchemy(app)

class Projects(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(255))
    title = db.Column(db.String(255))
    keywords=db.Column(db.String(255))
    objective = db.Column(db.String(1000))
    description=db.Column(db.String(1000))
    requirement=db.Column(db.String(1000))
    announcement=db.Column(db.String(1000))
    score = db.Column(db.Integer)
    date = db.Column(db.Integer)
    owner=db.Column(db.Integer)

    
    def __init__(self, email, title, keywords, objective, description, requirement, announcement,owner):
        self.email=email
        self.title=title
        self.keywords=keywords
        self.objective=objective
        self.description=description
        self.requirement=requirement
        self.announcement=announcement
        self.score=3
        self.date=int(time())
        self.owner=owner


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
        except:
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

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


def emailHandler(email):
    if "cmu.edu" in email:
        return email
    return None

def keywordsHandler(keywords):
    return keywords.replace(",",";")

def contentHandler(content):
    "Takes the string after post/ and returns a posts object"
    email=emailHandler(content["q1"])
    title=content["q2"]
    keywords=keywordsHandler(content["q3"])
    objective=content["q4"]
    description=content["q5"]
    requirement=content["q6"]
    announcement=content["q7"]
    owner=getCurrentUserID()
    if email:
        return Projects(email,title,content["q3"],objective,description,requirement,announcement,owner)
    else:
        return None

def searchHandler(content):
    keywords=content.split(" ")
    return [keywords[i] for i in xrange(len(keywords)) if keywords[i]!=""]

def wordSearch(word,item):
    return (word in item.description.lower()) or (word in item.requirement.lower()) or (word in item.keywords.lower()) or (word in item.objective.lower())  or (word in item.announcement.lower()) or (word in item.title.lower())

def compareScore(left,right):
    return cmp(-left.score,-right.score)

def compareDate(left,right):
    return cmp(-left.date,-right.date)

def getCurrentUserID():
    try:
        return User.query.filter_by(name=current_user.name).first().ID
    except:
        return -1


@app.route('/')
@app.route('/index')
@login_required
def index():
    post=Projects.query.order_by(Projects.score).limit(9).all()
    #post on the main page, recent for the search box
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html", posts=post,recents=recent,userid=getCurrentUserID())

#These two below are for creating new Projects
@app.route('/create')
@login_required
def create():
    return render_template("create.html")

@app.route('/newpost', methods=["POST"]) 
@login_required
def newpost():
    newProject=contentHandler(request.form)
    if newProject:
        db.session.add(newProject)
        db.session.commit()
    return redirect(url_for("index"))

@app.route('/search', methods=["POST"])
@login_required
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
    return render_template("index.html",posts=result,recents=recent,userid=getCurrentUserID())

@app.route('/detail/<int:ID>')
@login_required
def detail(ID):
    result=[Projects.query.get(ID)]
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html",posts=result,recents=recent,userid=getCurrentUserID())


@app.route("/usr/<int:user_id>")
@login_required
def user(user_id):
    result=Projects.query.filter_by(owner=user_id).all()
    recent=Projects.query.filter(Projects.date>time()-86400*15).order_by(-Projects.date).limit(5).all()
    return render_template("index.html",posts=result,recents=recent,userid=user_id)

@app.route('/fblogin')
def fblogin():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/fblogin/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    fbuser=User.verify(me.data['id'], me.data['id'])
    if fbuser == False: 
        fbuser=User.add(me.data['id'], me.data['id'])
    login_user(fbuser)
    return redirect(url_for("index"))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0')

