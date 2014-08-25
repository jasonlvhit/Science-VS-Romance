import sae
from SvsR import app
from sae.ext.shell import ShellMiddleware

application = sae.create_wsgi_app(app)
application = sae.create_wsgi_app(ShellMiddleware(app))
