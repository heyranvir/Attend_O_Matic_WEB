from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# Define the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)
# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	attendance = db.relationship("Attendance", back_populates="student")

	def __repr__(self):
		return f'<Student {self.name}>'

# Define Attendance model
class Attendance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date, nullable=False)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	student = db.relationship("Student", back_populates="attendance")

	def __repr__(self):
		return f'<Attendance {self.date}>'

# Define route for home page
@app.route('/')
@app.route('/home')
def home():
	Stds = Student.query.all()
	return render_template('home.html', stds=Stds)

@app.route('/<int:id>/profile')
def profile(id):
	Std = Student.query.filter_by(id=id).first()
	attendance = Attendance.query.filter_by(student_id=Std.id).all()
	return render_template('profile.html', std=Std, attendance = attendance, ta = len(attendance))

# Define route for adding a new student
@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
	if request.method == "POST":
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')
		course = request.form.get('course')
		std = Student(name=name, email=email, password=password)
		db.session.add(std)
		db.session.commit()
		return f'Student with name {name} added to database.'
	return render_template('addnew.html')

@app.route('/mark_attendance', methods=['GET','POST'])
def mark_attendance():
	if request.method == 'GET':
		return render_template('attendance.html')

	course = request.form.get('course')
	name = request.form.get('name')
	date_str = request.form.get('date')

	date = datetime.strptime(date_str, '%Y-%m-%d').date()

	std = Student.query.filter_by(name=name).first()
	attendance = Attendance(student_id = std.id,date = date)
	db.session.add(attendance)
	db.session.commit()

	return 'Attendance Marked successfully'

@app.route('/mark_today/<int:id>', methods=['GET','POST'])
def mark_today(id):
	date_str = str(datetime.today()).split()[0]
	date = datetime.strptime(date_str, '%Y-%m-%d').date()
	try:
		att = Attendance.query.filter_by(date = date, student_id = id).first()
		if att:
			return "Already Marked"
		else:
			stu = Student.query.filter_by(id=id).first()
			attendance = Attendance(student_id = stu.id,date = date)
			db.session.add(attendance)
			db.session.commit()
			return 'Marked'
	except:
		stu = Student.query.filter_by(id=id).first()
		attendance = Attendance(student_id = stu.id,date = date)
		db.session.add(attendance)
		db.session.commit()
		return 'Marked'

# Define route for getting a user by name
@app.route('/getuser')
def getuser():
	usr = Student.query.filter_by(name='Ranvir').first()
	return usr

if __name__ == '__main__':
	# Create an application context
	with app.app_context():
		# Create all database tables
		db.create_all()
	# Run the app
	app.run()

