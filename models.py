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
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """Create posts for users"""

    __tablename__ ='posts'

    id = db.Column(db.Integer, 
                   primary_key=True) 

    title = db.Column(db.Text, 
                     nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable = False,
                           default = datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
                        

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

        
