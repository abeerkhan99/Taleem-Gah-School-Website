from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from models import *

app = Flask(__name__)

api= Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://faiz:password@localhost/taleem-gah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    def put(self, id):
        """ convert JSON data sent by user to python format, 
            search if the student exists,
            if exists, update it with given information,
            if not, create and add student into database
        """
        data = request.get_json()

        student = StudentModel.query.filter_by(id=id).first()

        if student:
            student.price = data["price"]
            student.author = data["author"]
        else:
            student = StudentModel(id=id,**data)
 
        db.session.add(student)
        db.session.commit()
 
        return student.json()

    def delete(self, id):
        """ Search if the student exists in the database and deletes,
            else, returns error
        """
        student = StudentModel.query.filter_by(id=id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'student not found'},404
        

#adding endpoint for single student operations
api.add_resource(StudentView, '/student') 

if __name__ == '__main__':
    app.run(host='localhost', port=5000)