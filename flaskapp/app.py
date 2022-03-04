from enum import unique
from tokenize import String
from xml.dom import ValidationErr
from flask import Flask, redirect, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
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
        return f"{self.no} - {self.email} - {self.named}"

class vaccines(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    named = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> str:
        return f"{self.no} - {self.named} - {self.description}"

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
            raise ValidationErr ("user already registered with this email")
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for("login")) 

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
    return render_template('booking.html') 

@app.route('/Receipt', methods=['GET','POST'])
def reacipt():
    return render_template('Receipt.html')     

if __name__ == "__main__":
    app.run(debug=True, port=8000)