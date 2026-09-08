from flask import Flask
app = Flask(__name__)
from api.routes import bp
app.register_blueprint(bp)
@app.route('/')
def index(): return 'Cookie Runners HQ'
