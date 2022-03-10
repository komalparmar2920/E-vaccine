import email
from email import message
from flask import Flask, redirect, render_template, request, redirect
from email.headerregistry import Address
from email.policy import default
from enum import unique
from tokenize import String
from xml.dom import ValidationErr
from flask import Flask, redirect, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from sqlalchemy import exc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///eVaccine.db"
app.config['SECRET_KEY'] = "key321"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25),nullable=False, unique=True)
    named = db.Column(db.String(25), nullable=False) 
    password = db.Column(db.String(25), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.no} - {self.email} - {self.named} - {self.password}"

class vaccines(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    named = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return f"{self.no} - {self.named} - {self.description}"

class vform(db.Model, UserMixin):
    no = db.Column(db.Integer, primary_key=True) 
    fname = db.Column(db.String(25), nullable=False)
    named = db.Column(db.String(10), nullable=False) 
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    mno = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Integer, nullable=False)
    age = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(25), nullable=False) 
    gender = db.Column(db.String(10),nullable=False) 
    vname = db.Column(db.String(25), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
       return f"{self.no} - {self.fname} - {self.named} - {self.lname}- {self.email} -  {self.mno} - {self.dob} - {self.age} - {self.address} - {self.gender} - {self.vname}"

class sform(db.Model, UserMixin):
    no = db.Column(db.Integer, primary_key=True)
    vname = db.Column(db.String(15), nullable=False)
    cname = db.Column(db.String(25), nullable=False)
    stime = db.Column(db.Integer, nullable=False)
    vdoze = db.Column(db.String(10), nullable=False)
    
    def __repr__(self) -> str:
       return f"{self.no} - {self.vname} - {self.cname} - {self.stime} - {self.vdoze}"

class contact(db.Model, UserMixin):
     no = db.Column(db.Integer, primary_key=True)
     named = db.Column(db.String(10), nullable=False) 
     email = db.Column(db.String(25), nullable=False)
     message = db.Column(db.String(25), nullable=False)

     def __repr__(self) -> str:
         return f"{self.no} - {self.named} - {self.email} - {self.message}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('index.html')

@app.route('/registerUser', methods=['GET' , 'POST'])
def registerUser():
    if request.method=='POST':
        named = request.form['named']
        email = request.form['email']
        password = request.form['password']
        new_user = users(named=named, email=email, password=password)
        existing_user = users.query.filter_by(email=email).first()
        if(existing_user):
           return render_template('email.html')
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for("login")) 

@app.route('/addVaccine', methods=['GET' , 'POST'])
def addVaccineForm():
    return render_template('addVaccine.html')

@app.route('/addVaccineAction', methods=['GET' , 'POST'])
@login_required
def addVaccine():
    if request.method=='POST':
        named = request.form['named']
        desc = request.form['desc']
        new_vaccine = vaccines(named=named, description=desc)
        db.session.add(new_vaccine)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/search', methods=['GET' , 'POST'])
@login_required
def searchVaccine():
    if request.method=='POST':
        named = request.form['vaccine']
        vaccine = vaccines.query.filter_by(named=named).first()
        if(vaccine):
            return render_template('vaccineDesc.html', vaccine= vaccine)
        else:
            return render_template('noSuchVaccine.html')

@app.route('/registerVaccine', methods=['GET' , 'POST'])
@login_required
def registerVaccine():
    if request.method=='POST':
        return render_template('form.html')

@app.route('/login', methods=['GET' , 'POST'])
def login():
    return render_template('login.html')

@app.route('/loginUser', methods=['GET' , 'POST'])
def loginUser():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = users.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                return render_template('wrongPassword.html') 
    return redirect(url_for('register'))      

@app.route('/home', methods=['GET' , 'POST'])
@login_required
def home():
    return render_template('home.html') 

@app.route('/logout', methods=['GET' , 'POST'])
def logout():
    logout_user()
    return redirect(url_for('register'))

@app.route('/aboutUs', methods=['GET' , 'POST'])
def aboutUs():
    logout_user()
    return render_template('aboutUs.html')

@app.route('/form', methods=['GET','POST'])  
def form():
    return render_template('form.html')

@app.route('/booking', methods=['GET','POST'])
def booking():
    if request.method=='POST':
        fname=request.form['fname']
        named=request.form['named']
        lname=request.form['lname']
        email=request.form['email']
        mno=request.form['mno']
        dob=request.form['dob']
        age=request.form['age']
        address=request.form['address']
        gender = request.form['gender']
        vname = request.form['vname']
        eVaccine = vform(fname=fname, named=named, lname=lname, email=email, mno=mno, dob=dob, age=age, address=address, gender=gender, vname=vname)
        db.session.add(eVaccine)
        db.session.commit()
    
    
    return render_template('booking.html'  )

@app.route('/reacipt', methods=['GET','POST'])
def reacipt():
    if request.method=='POST':
        vname = request.form['vname']
        cname = request.form['cname']
        stime = request.form['stime']
        vdoze = request.form['vdoze']
        eVaccine = sform( vname=vname, cname=cname, stime=stime, vdoze=vdoze)
        db.session.add(eVaccine)
        db.session.commit()
       
    alltodo1 = vform.query.all()
    alltodo2 = sform.query.all()
    return render_template('reacipt.html', alltodo1=alltodo1, alltodo2=alltodo2) 

@app.route('/delete/<int:no>')
def delete(no):
        eVaccine = sform.query.filter_by(no=no).first()
        eVaccine = vform.query.filter_by(no=no).first()
        db.session.delete(eVaccine)
        db.session.commit()        
        return redirect('/reacipt')

@app.route('/update')
def update():
    return redirect("/form")        
        
@app.route('/feedback', methods=['GET','POST'])  
def feedback():
    return render_template('feedback.html') 

@app.route('/contact',methods=['GET','POST'])
def cont():
    if request.method=='POST':
        named = request.form['named']
        email = request.form['email']
        message = request.form['message']
        eVaccine = contact(named=named, email=email, message=message)
        db.session.add(eVaccine)
        db.session.commit()
    return render_template('update.html')    


if __name__ == "__main__":
    app.run(debug=True, port=8000)