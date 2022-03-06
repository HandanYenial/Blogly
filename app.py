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

#### Part 2: Add-Edit-Delete Posts

@app.route('/users/<int:user_id>/posts/new' , methods = ["GET"])
def show_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template("add_post.html", user=user)

@app.route('/users/<int:user_id>/posts/new' , methods = ["POST"])
def handle_form(user_id):
    """Handle add form,add post and redirect user to the info page"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    
    #new_post.title = request.form["title"]
    #new_post.content = request.form["content"]
    #new_post.created_at = request.form["created_at"] 

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>' , methods = ["GET"])
def show_post(post_id):
    """ Show a post"""
    post= Post.query.get_or_404(post_id)
    return render_template("show_post.html" , post = post)   

@app.route('/posts/<int:post_id>/edit' , methods=["GET"])
def show_edit_form(post_id):
    """Show a form to edit a post"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit' , methods = ["POST"])
def edit_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    #post.created_at = request.form["created_at"] 

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete' , methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")



