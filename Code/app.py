from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
#from flask_sqlalchemy import SQLAlchemy
from models import db, StudentModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/taleemgah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
migrate = Migrate(app, db)
api= Api(app)

db.init_app(app) #links database instance with api app

@app.before_first_request
def create_table():
    db.create_all()

class StudentsView(Resource):
    """ Get information of all students
    """
    def get(self):
        """ get all objects from StudentModel
            return the JSON text of all objects
        """
        students = StudentModel.query.all()
        return {'Students':list(x.json() for x in students)}
         
    def post(self):
        """convert the JSON data sent by the user to python-format
           create a new StudentModel object and send in the data
           save to DB
        """
        data = request.get_json()
        new_student = StudentModel(data['name'],data['age'])
        db.session.add(new_student)
        db.session.commit()
        return new_student.json(),201

#creating endpoint for viewing all students and adding students
api.add_resource(StudentsView, '/students')

class StudentView(Resource):
    """ Get, edit, delete Information of a single student
    """
    def get(self, name):
        """ Get the student with the given name and return it, else return 404 not found
        """
        student = StudentModel.query.filter_by(name=name).first()
        if student:
            return student.json()
        return {'message':'student not found'},404

    def put(self, name):
        """ convert JSON data sent by user to python format, 
            search if the student exists,
            if exists, update it with given information,
            if not, create and add student into database
        """
        data = request.get_json()

        student = StudentModel.query.filter_by(name=name).first()

        if student:
            student.name = data["name"]
            student.age = data["age"]
        else:
            student = StudentModel(name=name,**data)
 
        db.session.add(student)
        db.session.commit()
 
        return student.json()

    def delete(self, name):
        """ Search if the student exists in the database and deletes,
            else, returns error
        """
        student = StudentModel.query.filter_by(name=name).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'student not found'},404
        

#adding endpoint for single student operations
api.add_resource(StudentView, '/student/<string:name>') 

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
