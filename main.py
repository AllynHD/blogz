#add flash message to base next

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://blogz:allyn@localhost:8889/blogz"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'random'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user
        
    def __repr__(self):
        return '<Blog %r>' % self.title

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


#@app.before_request
#def require_login():
 #   allowed_routes = ['login', 'signup']
  #  if request.endpoint not in allowed_routes and 'username' not in session:
   #     return redirect('/login')

@app.route('/')
def kick():
    return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog():

    if request.method == 'GET':
        if 'id' in request.args:
            blog_id = request.args.get('id')
            blog = Blog.query.get(blog_id)
            return render_template('posts.html', title=blog.title, body=blog.body)
        else:
            posts = Blog.query.all()
            return render_template('blogs.html', title="Build-A-Blog!", posts=posts)
    
    username = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        title_error = ''    
        body_error = ''
        blog_title = request.form['title']
        blog_body = request.form['body']
        

        
    
    

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    
    username = User.query.filter_by(username = "allyn").first()
    
    if request.method == 'GET':
        title = request.args.get('title')
        body = request.args.get('body')
        title_error = request.args.get('title_error')
        body_error = request.args.get('body_error')
        if title_error == None and body_error == None:
            return render_template('newpost.html')
        if title_error == None:
            return render_template('newpost.html', body_error = body_error, title=title)
        if body_error == None:
            return render_template('newpost.html', title_error = title_error, body=body)
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ''
        body_error = ''
        if blog_title == '':
            title_error = "Please give your entry a title!"
        if blog_body == '':
            body_error = "Empty posts aren't posts. Please give me content."
        if title_error or body_error:    
            return redirect('/newpost?title_error=' + title_error + '&title=' + blog_title + '&body_error=' + body_error + '&body=' + blog_body)
        new_blog = Blog(blog_title, blog_body, username)
        db.session.add(new_blog)
        db.session.commit()
        blog = Blog.query.filter_by(title=blog_title).first()
        blog_id = str(blog.id)
        return redirect('/blog?id=' + blog_id)            

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        user_error = ''
        pw_error = ''
        ver_error = ''
        
        if username.isalpha() == False:
            user_error = "Username should be only alphabetic characters"
        if username == '':
            user_error = "Username, ergo sum. Or, 'Please enter a username.'"
        if len(password) < 3 or len(password) > 20 or " " in password:
            pw_error = "Password must be between 3 and 20 characters, and no spaces."
        if password == '':
            pw_error = "Please enter a Password!"
        if password != verify:
            ver_error = "Those passwords didn't match."
        if verify == '':
            ver_error = "I think you forgot to verify your password, bruh..."
        if user_error or pw_error or ver_error:
            user_name = username
            username = ''
            return render_template('signup.html', username=username, user_name=user_name, user_error=user_error, pw_error=pw_error, ver_error=ver_error)
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
        else:
            flash('User already exists', 'error')
            return render_template('signup.html')
    else:
        return render_template('signup.html')



@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/blog')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')

@app.route('/index')
def index():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    #delete session['email']
    #redirect to /blog
    pass


if __name__ == '__main__':
    app.run()