"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





ICON_URL = "https://icons.iconarchive.com/icons/dakirby309/windows-8-metro/256/Folders-OS-User-No-Frame-Metro-icon.png"

class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True) 

    first_name = db.Column(db.Text(15), 
                     nullable=False) 
                     

    last_name = db.Column(db.Text(15),
                     nullable=False) 
                 

    image_url = db.Column(db.Text, nullable=False, default= ICON_URL)
