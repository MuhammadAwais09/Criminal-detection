from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/criminaldata'  
db = SQLAlchemy(app)



class Criminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    father_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    crimes_done = db.Column(db.Text)
    profile_image = db.Column(db.LargeBinary)

def add_criminal():
    data = request.json
    new_criminal = Criminal(
        name=data['name'],
        father_name=data['father_name'],
        gender=data['gender'],
        dob=data['dob'],
        crimes_done=data['crimes_done'],
        profile_image=data['profile_image'],
    )
    db.session.add(new_criminal)
    db.session.commit()
    return jsonify({"message": "Criminal added successfully!"})



def get_criminals():
    criminals = Criminal.query.all()
    result = []
    for criminal in criminals:
        result.append({
            'id': criminal.id,
            'name': criminal.name,
            'father_name': criminal.father_name,
            'gender': criminal.gender,
            'dob': criminal.dob.strftime('%Y-%m-%d'),
            'crimes_done': criminal.crimes_done,
            'profile_image': criminal.profile_image,
        })
    return jsonify(result)


db.create_all()