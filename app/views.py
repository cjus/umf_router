"""Flash app views
Here the index route is setup to server index.html and our angularjs-based
web application. The web application is called UMFTester and is located under
app/static
"""
__author__ = 'carlosjustiniano'

from flask import render_template
from app import app


@app.route('/')
def index():
    """index.html router"""
    return render_template('index.html')
