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
    testttt="""<p>Climb leg make muffins or sweet beast play time and hate dog or chew foot. Stretch climb leg. Play time give attitude for all of a sudden go crazy chase imaginary bugs lick butt. Claw drapes burrow under covers so hide when guests come over, inspect anything brought into the house hopped up on goofballs. Nap all day swat at dog and rub face on everything stick butt in face all of a sudden go crazy need to chase tail yet rub face on everything. Give attitude chew iPad power cord, and stick butt in face or chase imaginary bugs. Hate dog destroy couch or under the bed and nap all day. Hate dog flop over and missing until dinner time. Chew iPad power cord stick butt in face so leave hair everywhere. Stretch swat at dog. Stand in front of the computer screen hunt anything that moves yet behind the couch or lick butt intrigued by the shower. Give attitude hate dog but chase imaginary bugs sleep on keyboard or play time. Intently stare at the same spot. Leave dead animals as gifts intently sniff hand for behind the couch intently stare at the same spot. Sun bathe make muffins. Use lap as chair hide when guests come over and hunt anything that moves make muffins. Use lap as chair. Lick butt flop over so behind the couch for intrigued by the shower leave dead animals as gifts for sleep on keyboard or play time. Run in circles find something else more interesting or need to chase tail for hopped up on goofballs for find something else more interesting. Leave hair everywhere sweet beast for leave hair everywhere for give attitude shake treat bag for throwup on your pillow for run in circles. Find something else more interesting inspect anything brought into the house, cat snacks why must they do that use lap as chair or run in circles. Claw drapes inspect anything brought into the house yet stand in front of the computer screen or behind the couch so give attitude all of a sudden go crazy. All of a sudden go crazy find something else more interesting or behind the couch intently sniff hand or stare at ceiling, and chase mice. Need to chase tail. Stretch. </p>
                            <p>Stick butt in face give attitude intrigued by the shower intently sniff hand. Lick butt run in circles. Leave hair everywhere sleep on keyboard. Intently sniff hand hopped up on goofballs so leave dead animals as gifts shake treat bag use lap as chair or inspect anything brought into the house. Intently sniff hand swat at dog hate dog throwup on your pillow and climb leg. Missing until dinner time throwup on your pillow cat snacks so stare at ceiling mark territory so play time. Hunt anything that moves run in circles or attack feet yet intrigued by the shower. Swat at dog sleep on keyboard. Hunt anything that moves hopped up on goofballs but leave hair everywhere give attitude. Behind the couch. Find something else more interesting chase imaginary bugs shake treat bag destroy couch or cat snacks lick butt, but hide when guests come over. Stick butt in face chase imaginary bugs for mark territory sleep on keyboard leave hair everywhere intrigued by the shower. Chew iPad power cord give attitude lick butt and hunt anything that moves. Leave hair everywhere intently stare at the same spot hate dog. Sweet beast chew foot. All of a sudden go crazy all of a sudden go crazy, but throwup on your pillow. Chew foot. Lick butt climb leg, but behind the couch but nap all day. Chase mice behind the couch. Mark territory attack feet or find something else more interesting so throwup on your pillow. Sun bathe play time so shake treat bag. Nap all day chase mice. </p>
                            <p>Hunt anything that moves hunt anything that moves burrow under covers and stick butt in face throwup on your pillow. Behind the couch claw drapes. Rub face on everything burrow under covers or intrigued by the shower. Mark territory destroy couch. Find something else more interesting. Find something else more interesting why must they do that give attitude yet chase mice behind the couch chase mice. Sun bathe. </p>
                            <p>Need to chase tail leave hair everywhere run in circles make muffins. Hunt anything that moves intently sniff hand and lick butt climb leg. Climb leg intently stare at the same spot stare at ceiling and stick butt in face find something else more interesting. Hopped up on goofballs missing until dinner time chase mice. Find something else more interesting burrow under covers inspect anything brought into the house intently stare at the same spot but leave dead animals as gifts. Stand in front of the computer screen swat at dog flop over or swat at dog. Inspect anything brought into the house chew iPad power cord yet chew foot, so hopped up on goofballs chew foot. Hate dog. Need to chase tail rub face on everything yet nap all day but sleep on keyboard attack feet or climb leg stretch. Chase mice hunt anything that moves for flop over hunt anything that moves intently sniff hand. Cat snacks play time. Throwup on your pillow hide when guests come over why must they do that. Stare at ceiling destroy couch destroy couch so shake treat bag, play time. Sleep on keyboard swat at dog and chew iPad power cord hate dog lick butt but nap all day. Shake treat bag. Chew iPad power cord intrigued by the shower for chase mice but flop over. Leave hair everywhere chase mice hate dog need to chase tail flop over. Stick butt in face all of a sudden go crazy give attitude or flop over. </p>
                            <p>Stretch hopped up on goofballs, destroy couch yet hate dog. Burrow under covers rub face on everything. Stick butt in face burrow under covers stand in front of the computer screen, make muffins yet chew iPad power cord. Play time find something else more interesting for missing until dinner time or intently stare at the same spot yet claw drapes yet leave hair everywhere. Why must they do that under the bed or hopped up on goofballs. Inspect anything brought into the house burrow under covers, stare at ceiling and cat snacks or stand in front of the computer screen yet chew iPad power cord play time. Under the bed run in circles yet cat snacks yet sweet beast. Shake treat bag need to chase tail burrow under covers so swat at dog. Leave hair everywhere. Missing until dinner time inspect anything brought into the house hopped up on goofballs all of a sudden go crazy. </p>
                            <p>Chew foot swat at dog. Attack feet hide when guests come over hide when guests come over, chew foot hide when guests come over. Sleep on keyboard chew iPad power cord so claw drapes intrigued by the shower for hunt anything that moves chew iPad power cord, sun bathe. Give attitude throwup on your pillow inspect anything brought into the house shake treat bag chase imaginary bugs yet give attitude. Stand in front of the computer screen claw drapes, for hate dog yet flop over behind the couch attack feet or mark territory. Chew iPad power cord intently sniff hand so rub face on everything or rub face on everything. Chew iPad power cord missing until dinner time climb leg, yet intrigued by the shower burrow under covers or nap all day, yet inspect anything brought into the house. Play time why must they do that cat snacks. Play time. Intently sniff hand sleep on keyboard. Chase mice leave hair everywhere yet mark territory chase imaginary bugs stick butt in face behind the couch and swat at dog. Under the bed all of a sudden go crazy but why must they do that. Make muffins. Cat snacks sun bathe. Missing until dinner time burrow under covers missing until dinner time hide when guests come over yet find something else more interesting stare at ceiling, or stretch. Intently stare at the same spot stick butt in face and stare at ceiling for chase mice for nap all day leave dead animals as gifts, chase imaginary bugs. Inspect anything brought into the house destroy couch so intently sniff hand so cat snacks nap all day but leave hair everywhere hide when guests come over. Behind the couch hunt anything that moves for behind the couch yet rub face on everything all of a sudden go crazy. Shake treat bag leave hair everywhere stick butt in face sun bathe. </p>
                            <p>Shake treat bag throwup on your pillow for sun bathe and intently stare at the same spot use lap as chair. Hunt anything that moves shake treat bag make muffins yet sleep on keyboard leave dead animals as gifts, or intently stare at the same spot. Hide when guests come over nap all day run in circles swat at dog yet use lap as chair for stick butt in face use lap as chair. Under the bed intently sniff hand yet under the bed. Play time intently stare at the same spot. Leave hair everywhere intently sniff hand flop over. Stand in front of the computer screen use lap as chair, but throwup on your pillow cat snacks or rub face on everything use lap as chair so chase mice. Hide when guests come over intently stare at the same spot hide when guests come over, for leave hair everywhere rub face on everything why must they do that. Burrow under covers rub face on everything attack feet, and find something else more interesting. Hunt anything that moves destroy couch for stick butt in face so sun bathe stand in front of the computer screen and rub face on everything. Cat snacks under the bed. Burrow under covers missing until dinner time run in circles yet hide when guests come over. Stare at ceiling hunt anything that moves for sun bathe but all of a sudden go crazy or all of a sudden go crazy flop over or intrigued by the shower. Leave hair everywhere intently stare at the same spot leave hair everywhere hate dog, and inspect anything brought into the house or sweet beast yet inspect anything brought into the house. Chase mice hopped up on goofballs yet burrow under covers for chase mice but hopped up on goofballs. </p>
                            <p>Chase mice play time hide when guests come over. Hunt anything that moves chew foot all of a sudden go crazy yet stare at ceiling, and destroy couch. Inspect anything brought into the house cat snacks missing until dinner time. Chew foot behind the couch for sleep on keyboard yet rub face on everything, hide when guests come over. Cat snacks lick butt hunt anything that moves. Why must they do that need to chase tail cat snacks hunt anything that moves hunt anything that moves give attitude run in circles. Find something else more interesting intently sniff hand and sun bathe. Leave hair everywhere lick butt, for need to chase tail but intrigued by the shower for mark territory sweet beast. Stretch sleep on keyboard leave dead animals as gifts but climb leg so sleep on keyboard but stare at ceiling. Claw drapes intrigued by the shower hide when guests come over yet use lap as chair. Throwup on your pillow leave hair everywhere sweet beast. Under the bed. Stand in front of the computer screen. Stand in front of the computer screen stretch so chase imaginary bugs. Intently sniff hand stand in front of the computer screen. Chase imaginary bugs find something else more interesting. Burrow under covers shake treat bag. Attack feet stand in front of the computer screen under the bed why must they do that or cat snacks stick butt in face but hide when guests come over. All of a sudden go crazy hopped up on goofballs yet intently sniff hand. Throwup on your pillow flop over chase imaginary bugs hunt anything that moves. Missing until dinner time make muffins and sun bathe. </p>
                            <p>Intently stare at the same spot chew iPad power cord burrow under covers or why must they do that or all of a sudden go crazy. Lick butt stretch but intrigued by the shower. Sleep on keyboard climb leg inspect anything brought into the house. Give attitude. Climb leg run in circles shake treat bag so hate dog for play time yet hide when guests come over. Why must they do that hate dog attack feet intrigued by the shower, so rub face on everything. Sun bathe leave dead animals as gifts or attack feet. </p>
                            <p>Claw drapes burrow under covers. Nap all day. Need to chase tail chase mice stare at ceiling so hate dog or flop over hide when guests come over climb leg. Under the bed play time yet stick butt in face sun bathe but missing until dinner time. Stand in front of the computer screen why must they do that. Attack feet rub face on everything, shake treat bag, need to chase tail attack feet swat at dog use lap as chair. Leave dead animals as gifts attack feet claw drapes yet chase imaginary bugs. Stretch burrow under covers for chew iPad power cord or climb leg, for use lap as chair make muffins attack feet. Use lap as chair all of a sudden go crazy and run in circles for chase imaginary bugs, so climb leg and hide when guests come over. Chew foot chase mice. Make muffins. Intently sniff hand hate dog and why must they do that claw drapes. Give attitude mark territory intrigued by the shower and leave hair everywhere but destroy couch claw drapes inspect anything brought into the house. Stare at ceiling. Cat snacks inspect anything brought into the house destroy couch but destroy couch or mark territory yet hate dog yet flop over. Burrow under covers hide when guests come over swat at dog destroy couch nap all day or all of a sudden go crazy. Use lap as chair use lap as chair so sleep on keyboard, mark territory, and burrow under covers stand in front of the computer screen throwup on your pillow. Play time. Hopped up on goofballs lick butt chase imaginary bugs, yet swat at dog play time for chew iPad power cord. Stick butt in face. Missing until dinner time chew foot sleep on keyboard find something else more interesting intently sniff hand so lick butt. Throwup on your pillow. Intently sniff hand throwup on your pillow so play time but hopped up on goofballs nap all day so intrigued by the shower but burrow under covers.</p>"""
    test=[posts("abc","def",testttt,42)]*9
    return render_template("index.html", posts=test)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/newpost/<string:content>')
def newpost(content):
    newTitle = "abc"
    newSubtitle="def"
    newText=content
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
