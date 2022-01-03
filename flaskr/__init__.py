import os 
from flask import Flask

# function is an app factory, creates the application and all its configurations
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return ('Hello, World!')
    
    # registers DB commands with application
    from . import db
    db.init_app(app)

    # registers authentication BluePrint with application
    from . import auth
    app.register_blueprint(auth.bp)
    
    # registers image_editing Blueprint with app
    from . import image_editing
    app.register_blueprint(image_editing.bp)
    # places image_editing index as the main index of the page, i.e. at /
    app.add_url_rule('/', endpoint='index')

    return app
