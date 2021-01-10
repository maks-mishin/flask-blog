import json
import os
import sqlite3
from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from init_db import Post

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['JSON_AS_ASCII'] = False

basedir = os.path.abspath(os.path.dirname(__file__))
path_db = 'sqlite:///' + os.path.join(basedir, 'database.db?check_same_thread=False')
engine = create_engine(path_db)

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def index():
    posts = session.query(Post).all()
    return render_template('index.html', posts=posts)


@app.route('/api/posts')
def api_index():
    posts = session.query(Post).all()

    json_posts = []
    for post in posts:
        json_posts.append({
            "id": post.id,
            "text": post.text,
            "title": post.title,
            "date": post.date
        })
    return jsonify(json_posts)


@app.route('/api/posts/<int:post_id>')
def api_post(post_id):
    post = session.query(Post).filter_by(id=post_id).one()
    return jsonify({
        "id": post.id,
        "text": post.text,
        "title": post.title,
        "date": post.date
    })


@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    one_post = Post.query.get_or_404(id=post_id)
    return render_template('post.html', post=one_post)


@app.route('/new', methods=('GET', 'POST'))
def new_post():
    if request.method == 'POST':
        title_request = request.form['title']
        text_request = request.form['content']

        if title_request == "" or text_request == "":
            return redirect(url_for('new_post'))
        post = Post.query.create(title=title_request, text=text_request)

        session.add(post)
        session.commit()
        return redirect(url_for("index"))

    return render_template('create.html')


@app.route('/api/posts/new', methods=['POST'])
def api_new_post():
    if not request.json or "title" not in request.json or "text" not in request.json:
        abort(400)
    
    title_request = request.json['title']
    text_request = request.json['text']

    if title_request == "" or text_request == "":
        return redirect(url_for('api_index'))
    post = Post.query.create(title=title_request, text=text_request)

    session.add(post)
    session.commit()
    return redirect(url_for("api_index"))


@app.route('/posts/<int:post_id>/edit', methods=('GET', 'POST'))
def post_edit(post_id):
    edited_post = Post.query.get_or_404(id=post_id)

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['content']

        if title == "" or text == "":
            return redirect(url_for('post_edit'))

        edited_post.title = title
        edited_post.text = text
        return redirect(url_for('index'))
    return render_template('edit.html', post=edited_post)


@app.route('/posts/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    deleted_post = Post.query.get_or_404(id=post_id)
    session.delete(deleted_post)
    session.commit()
    return redirect(url_for("index"))


# api_delete - добавить

if __name__ == '__main__':
    app.run(debug=True)
