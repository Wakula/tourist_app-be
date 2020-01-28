from flask import Flask, send_from_directory
from apps import APPS
from database import set_db


def _setup_blueprints(main_app, app_list):
    for app in app_list:
        app.setup_urls()
        app.setup_controllers()
        app.setup_models()
        main_app.register_blueprint(app, url_prefix=f'/api/{app.name}')


def create_app(config):
    main_app = Flask(__name__)
    main_app.config.from_object(config)
    _setup_blueprints(main_app, APPS)
    main_app.app_context().push()
    set_db(main_app)
    return main_app


if __name__ == '__main__':
    from config import DebugConfig
    app = create_app(DebugConfig)
    # only for development
    from flask_cors import CORS
    CORS(app)



    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)

    app.run()
