from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:jim@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY'] = True
db = SQLAlchemy(app)


class Blogs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/")
def index():
    return redirect("/blog")

@app.route('/blog', methods=['POST', 'GET'])
def blog_display():

    if request.args:
        blog_id = request.args.get('id')
        blog_post = Blogs.query.get(blog_id)
        return render_template('blogentry.html', title="Blog Entry", blog_post=blog_post, blog_id=blog_id)

        blog = Blogs.query.all()
        return render_template('blog.html', blog=blog)

    else:  
        blog = Blogs.query.all()
        return render_template('blog.html', title= 'Build a Blog', blog=blog)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'GET':
        return render_template('newpost.html')

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        

        title_error=''
        body_error=''

        if len(title) == 0:
            title_error = "Enter a title!"
        if len(body) == 0:
            body_error == "Enter text for your post!"

        if title_error or body_error:
            return render_template('newpost.html', titlebase="New Entry", title_error= title_error, body_error=body_error, title=title, body=body)

        else:
            if len(title) and len(body) > 0:
                new_post = Blogs(title, body)
                db.session.add(new_post)
                db.session.commit()
                return redirect("/blog?id=" + str(new_post.id))

                
if __name__ == '__main__':
    app.run()