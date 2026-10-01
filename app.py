"""
AGRI-MITRA Application Factory and Entrypoint
Smart Agriculture Prediction & Recommendation Platform
"""

import os
from pathlib import Path
from flask import Flask, render_template, session
from config import Config
from database.db import init_db, db
from models.database_models import User


def create_app(config_class=Config, config_override=None):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if config_override:
        app.config.update(config_override)

    # Ensure required runtime directories exist
    Path(app.config['REPORT_DIR']).mkdir(parents=True, exist_ok=True)
    Path(app.config['EXPORT_DIR']).mkdir(parents=True, exist_ok=True)
    Path(app.config.get('UPLOAD_DIR', Path(__file__).resolve().parent / 'uploads')).mkdir(parents=True, exist_ok=True)
    (Path(__file__).resolve().parent / 'instance').mkdir(parents=True, exist_ok=True)

    # Initialize Database
    init_db(app)

    # Context processor for global template access
    @app.context_processor
    def inject_user_context():
        current_user = None
        if 'user_id' in session:
            current_user = User.query.get(session['user_id'])
        return dict(
            current_user=current_user,
            is_authenticated=('user_id' in session),
            is_admin=(session.get('role') == 'admin')
        )

    # Register Route Blueprints
    from routes.home_routes import home
    from routes.auth_routes import auth
    from routes.dashboard_routes import dashboard
    from routes.crop_routes import crop
    from routes.fertilizer_routes import fertilizer
    from routes.history_routes import history
    from routes.profile_routes import profile
    from routes.report_routes import report
    from routes.export_routes import export
    from routes.admin_routes import admin

    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(crop)
    app.register_blueprint(fertilizer)
    app.register_blueprint(history)
    app.register_blueprint(profile)
    app.register_blueprint(report)
    app.register_blueprint(export)
    app.register_blueprint(admin)

    # System Health Check
    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'platform': 'AGRI-MITRA',
            'database': 'connected',
            'models': {
                'crop_rf': Path(app.config['CROP_MODEL_PATH']).exists(),
                'fertilizer_rf': Path(app.config['FERTILIZER_MODEL_PATH']).exists()
            }
        }

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(host='127.0.0.1', port=port, debug=debug)
