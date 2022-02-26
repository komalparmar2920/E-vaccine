from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///eVaccine.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    named = db.Column(db.String(25), primary_key=True)
    email = db.Column(db.String(25), nullable=False) 
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
 
@app.route('/login', methods=['GET' , 'POST'])
def register():
    if request.method=='POST':
        named = request.form['named']
        email = request.form['email']
        password = request.form['password']
        xyz = users(named=named, email=email, password=password)
        db.session.add(xyz)
        db.session.commit()
    return render_template('login.html') 
    
@app.route('/home', methods=['GET','POST'])
def home():
  return render_template('home.html')

@app.route('/form', methods=['GET','POST'])  
def form():
    return render_template('form.html')

@app.route('/booking', methods=['GET','POST'])
def booking():
    return render_template('booking.html') 

@app.route('/Reacipt', methods=['GET','POST'])
def reacipt():
    return render_template('reacipt.html')       

if __name__ == "__main__":
    app.run(debug=True, port=8000)