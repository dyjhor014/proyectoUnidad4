from datetime import datetime
from app import db

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    nombre = db.column(db.String(100))
    locacion = db.column(db.String(30))
    informacion = db.Column(db.String(250))
    fecha_creacion = db.Column(db.DateTime())
    ultima_conexion = db.column(db.DateTime())
    avatar = db.column(db.String(300))
    
    