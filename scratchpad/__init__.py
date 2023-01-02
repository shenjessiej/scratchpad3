import os

from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'scratchpad.sqlite'),
    )

    from . import db 
    db.init_app(app)

    from . import post 
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')

    return app

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
