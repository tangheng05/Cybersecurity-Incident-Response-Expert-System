import os
from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions import db, csrf


def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.rule_routes import rule_bp
    from app.routes.attack_type_routes import attack_type_bp
    from app.routes.alert_routes import alert_bp
    from app.routes.incident_routes import incident_bp
    from app.routes.role_routes import role_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(attack_type_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(role_bp)

    # Root route redirects to dashboard
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Create tables
    with app.app_context():
        from app.models import User, AttackType, Rule, Alert, Incident, IncidentHistory  # noqa: F401
        db.create_all()

    return app
