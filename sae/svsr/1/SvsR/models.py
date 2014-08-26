from SvsR import db

post_tag_re = db.Table('post_tag', 
						db.Column('id', db.Integer, primary_key = True),
						db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
						db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
			)

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(200))
	content = db.Column(db.Text)
	pub_time = db.Column(db.DateTime)

	def __init__(self, title, content, pub_time):
		self.title = title
		self.content = content
		self.pub_time = pub_time
	
	def __le__(self, other):
		return self.pub_time > other.pub_time

	def __repr__(self):
		return '<Post %r>' % self.title

class Tag(db.Model):
	__tablename__ = 'tag'
	id = db.Column(db.Integer, primary_key = True)
	tag_name = db.Column(db.String(40))
	
	posts = db.relationship('Post', secondary = post_tag_re, backref = db.backref('tag', lazy = 'dynamic'))

	def __init__(self, tag_name):
		self.tag_name = tag_name
	
	def __le__(self, other):
		return len(self.posts) > len(other.posts)

	def __repr__(self):
		return '<Tag %r>' % self.tag_name
