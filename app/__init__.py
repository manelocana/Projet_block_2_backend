
from flask import Flask
from app.routes.home import home_bp
from app.routes.pages import pages_bp
from app.routes.portfolio import portfolio_bp
from app.routes.blog import blog_bp
from app.routes.contact import contact_bp

from app.routes.auth import auth_bp
from app.routes.admin_routes import admin_bp

from app.extensions import db, login_manager

from config import Config

from flask_migrate import Migrate


migrate = Migrate()



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(home_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(contact_bp)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
