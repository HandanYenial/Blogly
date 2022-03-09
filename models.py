"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


ICON_URL = "https://icons.iconarchive.com/icons/dakirby309/windows-8-metro/256/Folders-OS-User-No-Frame-Metro-icon.png"

class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True) 

    first_name = db.Column(db.Text, 
                           nullable=False) 
                     

    last_name = db.Column(db.Text,
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


#There should also be a model for PostTag, which joins together a Post and a Tag. 
#It will have foreign keys for the both the post_id and tag_id. 
#Since we don’t want the same post to be tagged to the same tag more than once, 
#we’ll want the combination of post + tag to be unique. It also makes sense that neither 
#the post_id nor tag_id can be null.Add relationships so you can see the .tags for a post, and the .posts for a tag.

class PostTag(db.Model):
    """Post tag joins together a post and a tag"""

    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)

class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )

  


    

        
