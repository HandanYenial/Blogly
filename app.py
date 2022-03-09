"""Blogly application."""

from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db,User,Post, Tag, PostTag

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
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts_homepage.html", posts=posts)


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
    tag_ids = [int(num) for num in request.form.getlist("tags")] #####?
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
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
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit' , methods = ["POST"])
def edit_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    #post.created_at = request.form["created_at"] 
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete' , methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")  #why do i need to use f string here?


############################PART3

@app.route('/tags' , methods=["GET"])
def list_tags():
    """Lists all tags"""
    tags = Tag.query.all()
    return render_template('tags.html' , tags=tags)

@app.route('/tags/<int:tag_id>' , methods = ["GET"])
def show_tags(tag_id):
     """Show detail about a tag"""
     tag = Tag.query.get_or_404(tag_id)
     return render_template('show_tag.html' , tag=tag)

@app.route('/tags/new' , methods=["GET"])
def show_add_new_tag_form():
    """Shows a form to add a new tag"""
    posts = Post.query.all()
    return render_template('new_tag.html' , posts=posts)

@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Process add form, adds tag, and redirect to tag list."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):

    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit' , methods=["GET"])
def edit_form_for_tags(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tags.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Editing a tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):
    """Delete a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
   
    return redirect("/tags")



