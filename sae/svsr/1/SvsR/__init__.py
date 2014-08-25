from flask import Flask

from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
app.config.from_envvar('DOU_SETTINGS', silent = True)

class nullpool_SQLAlchemy(SQLAlchemy): 
	def apply_driver_hacks(self, app, info, options): 
		super(nullpool_SQLAlchemy, self).apply_driver_hacks(app, info, options) 
		from sqlalchemy.pool import NullPool 
		options['poolclass'] = NullPool 
		del options['pool_size']
#database
db = nullpool_SQLAlchemy(app)

from SvsR import views

