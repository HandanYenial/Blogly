"""Blogly application."""

from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db,User

app = Flask(__name__)

def connect_db(app):
    db.app = app
    db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "very-secret-key12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def redirect_users():
    """Redirect the list of users"""

    return redirect ('/users')


@app.route('/users')
def list_users():
    """Shows list of all users in db"""

    users = User.query.all() 
    return render_template('list.html', users=users) 


@app.route('/users/new' , methods=['GET'])
def add_new_user_form():
    """Show an add form for users"""
    return render_template('add_user.html')


@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Process the add form, adding a new user"""
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] 

    new_user  = User(first_name=first_name, last_name=last_name , image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template("info.html", user=user)

@app.route("/users/<int:user_id>/edit" , methods=["GET"])
def show_edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html" , user=user)
 

@app.route("/users/<int:user_id>/edit" , methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"] 

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete' , methods=["POST"])
def delete_user(user_id):
     user = User.query.get_or_404(user_id)
     db.session.delete(user)
     db.session.commit()

     return redirect("/users")
