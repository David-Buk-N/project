from flask import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename, send_from_directory
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form
from wtforms import *
from flask_wtf.file import *
from wtforms.validators import *
from enum import Enum
from flask_migrate import *
from datetime import datetime
from .app import fin_AsistsForm
import os 


#basedir = os.path.abspath(os.path.dirname(__file__))

# Instanstiate the app
app = Flask(__name__)

# Define DataBase connection
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///finance.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set access key
app.config['SECRET_KEY'] = 'Fantastic 11'
UPLOAD_FOLDER ='uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# Routes-----------------------------------------------------------------------------------------------------------------------------

# Define my Index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    if form.validate_on_submit():
        # Process the form data
        pass
    form = fin_AsistsForm()
    return render_template('index2.html',form=form)

@app.route('/financialAid')
def financialAid():
    financialAid = fin_Aid.query.all()
    return render_template('index.html', financialAid=financialAid)

@app.route('/finform')
def view_fin_form():
    form = fin_Form()
    return render_template('view_fin_form.html', form=form)

# Search functionality.
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    if query:
        # Filter bursaries based on search query
        results = fin_Aid.query.filter(fin_Aid.name.ilike(f"%{query}%")).all()
    else:
        results = fin_Aid.query.all()  # Display all bursaries if no query provided
    return render_template('search_results.html', results=results)

@app.route('/fin_upload', methods=['POST'])
def upload_doc():
    title = request.forms['title']
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        return 'No file uploaded'

@app.route('/download/<filename>', methods=['GET'])
def download_filename(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)



# Create models and Forms ------------------------------------------------------------------------------------------------------------

#Enum for userRole
class role(Enum):
    Admin = 'Admin'
    Student = 'Student'
    Donor = 'Donor'

#Base Model for users
class users(db.Model):
    __tablename__ = 'User'
    user_Id = db.Column(db.Integer, primary_key=True)
    user_Name = db.Column(db.String(50), unique = True, nullable=False)
    email = db.Column(db.String(50),unique = True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    role = db.Column(db.Enum(role))

#Base Model for Financial Aid(Superclass)
class fin_Aid(db.Model):
    __tablename__ = 'Financial Aid'
    fin_Id = db.Column(db.Integer, primary_key=True)
    fin_Name = db.Column(db.String(50), unique = True, nullable=False)
    fin_Description = db.Column(db.String(1000), nullable=False)
    fin_Doc = db.Column(db.String(255), nullable=False)
    fin_path = db.Column(db.String(255), nullable=False)
    upload_Date = db.Column(db.DateTime(datetime.date), nullable=False)
    expiry_Date = db.Column(db.DateTime(datetime.date), nullable=False)

    # Relationships


    def countdown_to_expiry(deadline_Date):
        # Parse the expiry date string into a datetime object
        deadline_Date = datetime.strptime(deadline_Date, '%Y-%m-%d %H:%M:%S')

        # Get the current datetime
        current_datetime = datetime.now()

        # Calculate the time difference (timedelta) between expiry datetime and current datetime
        time_difference = deadline_Date - current_datetime

        #Extract days, hours, minutes, and seconds from the timedelta
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)

        # Format the remaining time as a string
        remaining_time_str = f"{days} days, {hours} hours"

        return remaining_time_str

    def __repr__(self):
        return '<Grant %r>' %self.facualty_Name


# Financial Aid upload form
class fin_Form(Form):
    Name = StringField('Bursary Name', validators=[DataRequired()])
    document_type = SelectField('Type of Document', choices=[('bursary', 'Bursary'), ('scholarship', 'Scholarship'), ('grants', 'Grants')], validators=[DataRequired()])
    Description = TextAreaField('Description')
    upload_Date = DateField('Upload Date', validators=[DataRequired()], format='%Y-%m-%d')
    expiry_date = DateField('Expiry Date', validators=[DataRequired()], format='%Y-%m-%d')
    fin_Doc = FileField('Document', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])



#Base Model for Donor
class donor(db.Model):
    __tablename__ = 'Donor'
    donor_Id = db.Column(db.Integer, primary_key=True)
    donor_Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Grant %r>' %self.donor_Name
    


#---------------------------------------------------------------------------------------------------------------------------
# Student Side

# Financial Assistance Application
# Finance Assistance model
class fin_Asist(db.Model):
    __tablename__ = 'Financial Assistance'
    fin_Assist_Id = db.Column(db.Integer, primary_key=True)
    fin_Assist_Name = db.Column(db.String(50), nullable=False)
    fin_Assist_Surname = db.Column(db.String(50), nullable=False)
    fin_Assist_StudentNo = db.Column(db.String(13), nullable=False)
    fin_Assist_Phonenumber = db.Column(db.String(10), nullable=False)
    fin_Assist_Email = db.Column(db.String(100), nullable=False)
    fin_Assist_FinState = db.Column(db.String(255), nullable=False)
    fin_Assist_FinStatePath = db.Column(db.String(255), nullable=False)
    fin_Assist_ProfofReg = db.Column(db.String(255), nullable=False)
    fin_Assist_ProfofRegPath = db.Column(db.String(255), nullable=False)
    fin_Assist_Letter = db.Column(db.String(500), nullable=False)
    upload_Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    # Relationships


    def __repr__(self):
        return '<Grant %r>' %self.facualty_Name


# Create Financial Assistance upload form
class fin_AsistsForm(Form):
    Name = StringField('Name', validators=[DataRequired()])
    Surname = StringField('Surname', validators=[DataRequired()])
    Cellnumber = StringField('cellnumber', validators=[DataRequired()])
    email = EmailField('cellnumber', validators=[DataRequired()])
    upload_Date = DateField('Upload Date', validators=[DataRequired()], format='%Y-%m-%d')
    Proof_Reg = FileField('Proof of Registration', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])]) 
    fin_State = FileField('Document', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])



# Financial Aid Application
# Application model
class fin_App(db.Model):
    fin_App_Id = db.Column(db.Integer, primary_key=True)
    fin_App_Name = db.Column(db.String(50), nullable=False)
    fin_App_Surname = db.Column(db.String(50), nullable=False)
    assistance_type = db.Column(db.String(50), nullable=False)
    fin_App_Phonenumber = db.Column(db.String(10), nullable=False)
    fin_App_email = db.Column(db.String(100), nullable=False)
    fin_App_ProfofReg = db.Column(db.String(255), nullable=False)
    fin_App_ProfofRegPath = db.Column(db.String(255), nullable=False)
    fin_App_FinState = db.Column(db.String(255), nullable=False)
    fin_App_FinStatePath = db.Column(db.String(255), nullable=False)
    upload_Date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    # Relationships


    def __repr__(self):
        return '<Grant %r>' %self.facualty_Name


# Financial Aid Application upload form
class fin_AppForm(Form):
    Name = StringField('Name', validators=[DataRequired()])
    Surname = StringField('Surname', validators=[DataRequired()])
    cellnumber = StringField('cellnumber', validators=[DataRequired()])
    email = EmailField('cellnumber', validators=[DataRequired()])
    BankState = FileField('Document', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    Proof_Reg = FileField('Proof of Registration', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])]) 



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
