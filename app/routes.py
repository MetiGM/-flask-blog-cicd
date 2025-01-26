from flask import render_template, request, redirect, flash
from app import app, db
from app.models import Post, User

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Vulnerable raw SQL query (SQLi)
        user = db.engine.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'").fetchone()
        if user:
            flash('Logged in successfully!', 'success')
            return redirect('/')
        else:
            flash('Login failed!', 'danger')
    return render_template('login.html')

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # No input sanitization (XSS)
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added!', 'success')
        return redirect('/')
    return render_template('add_post.html')

@app.route('/delete-post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # No authentication check (IDOR)
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect('/')