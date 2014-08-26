from flask import render_template, request, redirect, url_for
from SvsR import app, db
from models import Post, Tag
from datetime import datetime
from mistune import markdown

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/archive')
def archive():
	p = Post.query.all()
	p.sort()	
	print(p)
	return render_template('post_list.html', items = p)

def tagFilter(tags):
	l = tags.strip().split(' ')
	s = set([i.tag_name for i in Tag.query.all()])
	for i in l:
		if i not in s:
			db.session.add(Tag(i))
			db.session.commit()
	return [i for i in Tag.query.all() if i.tag_name in set(l)]

@app.route('/create_post', methods = ['POST', 'GET'])
def create_post():
	if request.method == 'GET':
		return render_template("edit.html")
	assert request.method == 'POST'
	title = request.form['title']
	tags = tagFilter(request.form['tag'])
	content = request.form['editor'] 
	post = Post(title, content, datetime.now())
	for i in tags:
		post.tag.append(i)
	db.session.add(post)
	db.session.commit()
	return redirect(url_for('post', post_id = post.id))


@app.route('/post/<int:post_id>')
def post(post_id):
	p = Post.query.get(post_id)
	return render_template("post.html", title = p.title, content = markdown(p.content), pub_date = p.pub_time)

@app.route('/music')
def music():
	p = Tag.query.filter_by(tag_name = 'music').first().posts
	return render_template("post_list", items = p)

@app.route('/tags')
def tags():
	tags = Tag.query.all()
	tags.sort()
	return render_template("tag_list.html", tags = tags)

@app.route('/tag/<int:tag_id>')
def tag(tag_id):
	p = Tag.query.get(tag_id).posts
	return render_template("post_list.html", items = p)
