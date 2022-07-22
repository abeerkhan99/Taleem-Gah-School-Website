from flask_sqlalchemy import SQLAlchemy
#from app import db

db = SQLAlchemy()

class StudentModel(db.Model):
    """ Database table to store information of students
    """
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))   #more to be added
    age = db.Column(db.Integer())

    def __init__(self, name, age):
        """ Initialise table values
        """
        self.name = name  #more to be added
        self.age = age

    def json(self):
        """APIs use JSON for accepting and returning requests, this function returns the database
           information in json format. 
        """
        return {"name":self.name, "age":self.age}

# class Login_info(db.Model):
#     """ Database table to store login information for users of web app
#     """
#     pass



