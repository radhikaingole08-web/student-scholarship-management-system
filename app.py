from flask import Flask, request, jsonify
from flask_cors import CORS

from db import db
from models import Student, Scholarship, Application, Admin

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Suzan%40123@localhost/scholarship_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Student Scholarship Backend Running"


# ---------------- REGISTER ---------------- #

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    existing = Student.query.filter_by(email=data['email']).first()

    if existing:
        return jsonify({"message": "Email already exists"}), 400

    student = Student(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        cgpa=float(data['cgpa']),
        category=data['category'],
        mobile=data['mobile'],
        gender=data['gender'],
        year_of_study=str(data['year_of_study'])
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Registration Successful"})


# ---------------- LOGIN ---------------- #

# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['POST'])
def login():

    data = request.json

    student = Student.query.filter_by(
        email=data['email'],
        password=data['password']
    ).first()

    if student:
        return jsonify({
            "message": "Login Successful",
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email
        }), 200

    return jsonify({
        "message": "Invalid Email or Password"
    }), 401


# ---------------- SCHOLARSHIPS ---------------- #

@app.route('/scholarships', methods=['GET'])
def scholarships():

    scholarships = Scholarship.query.all()

    result = []

    for s in scholarships:
        result.append({
            "scholarship_id": s.scholarship_id,
            "title": s.title,
            "description": s.description,
            "amount": s.amount,
            "min_cgpa": s.min_cgpa
        })
        
    print(result)
    return jsonify(result)


# ---------------- ADD SCHOLARSHIP ---------------- #

@app.route('/add-scholarship', methods=['POST'])
def add_scholarship():

    data = request.json

    scholarship = Scholarship(
        title=data['title'],
        provider=data['provider'],
        description=data['description'],
        amount=float(data['amount']),
        min_cgpa=float(data['min_cgpa']),
        category=data['category'],
        last_date=data['last_date'],
        application_link=data['application_link']
    )

    db.session.add(scholarship)
    db.session.commit()

    return jsonify({
        "message": "Scholarship Added Successfully"
    })

@app.route('/apply-scholarship', methods=['POST'])
def apply_scholarship():

    data = request.json

    existing = Application.query.filter_by(
        student_id=data['student_id'],
        scholarship_id=data['scholarship_id']
    ).first()

    if existing:
        return jsonify({"message": "Already Applied"}), 400

    application = Application(
        student_id=data['student_id'],
        scholarship_id=data['scholarship_id']
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application Submitted Successfully"})

# ---------------- ADMIN LOGIN ---------------- #

@app.route('/admin-login', methods=['POST'])
def admin_login():

    data = request.json

    admin = Admin.query.filter_by(
        email=data['email'],
        password=data['password']
    ).first()

    if admin:
        return jsonify({
            "message": "Admin Login Successful",
            "admin_id": admin.admin_id,
            "name": admin.name
        })

    return jsonify({
        "message": "Invalid Admin Credentials"
    }), 401

# ---------------- VIEW ALL APPLICATIONS ---------------- #

@app.route('/applications', methods=['GET'])
def view_applications():

    applications = Application.query.all()

    result = []

    for app in applications:

        student = Student.query.get(app.student_id)
        scholarship = Scholarship.query.get(app.scholarship_id)

        result.append({
            "application_id": app.application_id,
            "student_name": student.name,
            "student_email": student.email,
            "scholarship_title": scholarship.title,
            "status": app.status
        })

    return jsonify(result)

# ---------------- APPROVE APPLICATION ---------------- #

@app.route('/approve-application/<int:application_id>', methods=['PUT'])
def approve_application(application_id):

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    application.status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Application Approved Successfully"
    })

# ---------------- REJECT APPLICATION ---------------- #

@app.route('/reject-application/<int:application_id>', methods=['PUT'])
def reject_application(application_id):

    application = Application.query.get(application_id)

    if not application:
        return jsonify({
            "message": "Application Not Found"
        }), 404

    application.status = "Rejected"

    db.session.commit()

    return jsonify({
        "message": "Application Rejected Successfully"
    })

# ---------------- VIEW ALL STUDENTS ---------------- #

@app.route('/students', methods=['GET'])
def view_students():

    students = Student.query.all()

    result = []

    for student in students:
        result.append({
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "cgpa": student.cgpa,
            "category": student.category,
            "mobile": student.mobile,
            "gender": student.gender,
            "year_of_study": student.year_of_study
        })

    return jsonify(result)

# ---------------- UPDATE SCHOLARSHIP ---------------- #

@app.route('/scholarship/<int:scholarship_id>', methods=['PUT'])
def update_scholarship(scholarship_id):

    scholarship = Scholarship.query.get(scholarship_id)

    if not scholarship:
        return jsonify({
            "message": "Scholarship Not Found"
        }), 404

    data = request.json

    scholarship.title = data['title']
    scholarship.provider = data['provider']
    scholarship.description = data['description']
    scholarship.amount = float(data['amount'])
    scholarship.min_cgpa = float(data['min_cgpa'])
    scholarship.category = data['category']
    scholarship.last_date = data['last_date']
    scholarship.application_link = data['application_link']

    db.session.commit()

    return jsonify({
        "message": "Scholarship Updated Successfully"
    })

# ---------------- DELETE SCHOLARSHIP ---------------- #
@app.route('/scholarship/<int:scholarship_id>', methods=['DELETE'])
def delete_scholarship(scholarship_id):

    scholarship = Scholarship.query.get(scholarship_id)

    if not scholarship:
        return jsonify({
            "message": "Scholarship Not Found"
        }), 404

    # Delete all applications related to this scholarship
    Application.query.filter_by(
        scholarship_id=scholarship_id
    ).delete()

    # Delete scholarship
    db.session.delete(scholarship)
    db.session.commit()

    return jsonify({
        "message": "Scholarship Deleted Successfully"
    })

if __name__ == '__main__':
    app.run(debug=True)