#password is 'allyn'
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:allyn@localhost:8889/build-a-blog"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET', 'POST'])
def blog():

    title_error = ''    
    content_error = ''
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_content = request.form['content']
        if blog_name == '':
            title_error = "Please give your entry a title!"
        if blog_content == '':
            content_error = "Empty posts aren't posts. Please give me content."
        if blog_name == '' or blog_content == '' :    
            return redirect('/newpost?title_error=' + title_error + '&name=' + blog_name + '&content_error=' + content_error + '&content=' + blog_content)

        new_blog = Blog(blog_name, blog_content)
        db.session.add(new_blog)
        db.session.commit()
    
    posts = Blog.query.all()
    return render_template('blogs.html', title="Build-A-Blog!", posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    
    if request.method == 'GET':
        name = request.args.get('name')
        content = request.args.get('content')
        title_error = request.args.get('title_error')
        content_error = request.args.get('content_error')
        if title_error == None and content_error == None:
            return render_template('newpost.html')
        if title_error == None:
            return render_template('newpost.html', content_error = content_error, name=name)
    else:
        name = ''
        content = ''
    return render_template('newpost.html', title_error = title_error, content_error = content_error, name = name, content = content)

if __name__ == '__main__':
    app.run()