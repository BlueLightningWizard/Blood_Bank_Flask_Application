from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

application = Flask(__name__)
application.debug = True

# Configuration for using a sqlite database
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blood_Bank.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(application)

# Migration
migrate = Migrate(application, db)

# Creating DB Model
class Donor(db.Model):
    
    ID = db.Column(db.Integer, primary_key=True)
    
    First_Name = db.Column(db.String(20), unique=False, nullable=False)
    Middle_Name = db.Column(db.String(20), unique=False, nullable=False)
    Last_Name = db.Column(db.String(20), unique=False, nullable=False)

    Blood_Group = db.Column(db.String(20), unique=False, nullable=False)

    Email = db.Column(db.String(100), unique=False, nullable=False)
    
    def __repr__(self):
        return f"Full Name : {self.first_name} {self.middle_name} {self.last_name} \nBlood Group: {self.blood_group}"

# Creating DB Instance
with application.app_context():
    db.create_all()

# Functions for Application
def index():
    return render_template('index.html')

def data():
    data = Donor.query.all()
    return render_template('data.html', data = data)

def add_data():
    first = request.form.get("first")
    middle = request.form.get("middle")
    last = request.form.get("last")
    blood_group = request.form.get("blood_group")
    email = request.form.get("email")

    if first != '' and middle != '' and last != '':
        
        data = Donor(First_Name = first, Middle_Name = middle, Last_Name = last, \
                     Blood_Group = blood_group, Email = email)
        
        db.session.add(data)
        db.session.commit()
        
        return redirect('/data')

    else:
        return redirect('/')

application.add_url_rule('/', 'index', index)
application.add_url_rule('/add_data', 'add_data', add_data, methods=['POST'])
application.add_url_rule('/data', 'data', data)

#Running the Application
if __name__ == '__main__':
    application.run()
