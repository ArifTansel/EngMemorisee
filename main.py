from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
import random

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Arif/Desktop/code/EngMemorisee/test.db'
db = SQLAlchemy(app)
app.secret_key="aaaaaaa"
class Words(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(80), unique=True, nullable=False)
    defination = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.term



@app.route("/") 
def index():
    session["change"] = 2
    session["answer"] = ""


    session["counter"] = -1
    word = Words.query.all()
    return render_template("index.html", word = word)

@app.route("/add" , methods=["POST"] )
def add():
    wordie=Words.query.all()
    try : 
        term = request.form.get("term").strip()
        defination = request.form.get("defination").strip()
        word = Words(term=term,defination=defination)
        db.session.add(word)
        db.session.commit()
        return redirect(url_for("index"))
    except :
        db.session.rollback()
        return render_template("index.html",Ierror=1,word=wordie)        



@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.session.delete(Words.query.filter_by(id=id).first())
    db.session.commit()
    return redirect(url_for("index"))




@app.route("/memorise/<int:i>", methods=["GET"])
def memorise(i):
    words  = Words.query.all()

    if i ==0 :
        session["question"] = random.sample(range(0,len(words)),len(words)-1)
        i+=1
    if session["change"] == 1 :
        session["counter"] +=1
        print("--------------------------")
    if session["counter"]>=len(words)-1:
        return redirect(url_for("index", Done = 1))

    print("--------------",session["change"])
    return render_template("memorise.html",right = session["change"],question = session["question"][session["counter"]] , word=words , answer = session["answer"] ) 





@app.route("/answer", methods=["POST"])
def answer():
    words  = Words.query.all()
    answer = request.form.get("answer")
    print(answer)
    if answer ==  words[session["question"][session["counter"]]].defination : #answer is true
        print("doğrudur")
        session["change"] = 1
        return redirect(url_for("memorise",i=1))
    else :                         #answer is false
        session["answer"] = answer
        session["change"] = 0
        return redirect(url_for("memorise",i=1))

if __name__ == "__main__":
    app.run(debug=True)#,host="192.168.43.46",port="9999"