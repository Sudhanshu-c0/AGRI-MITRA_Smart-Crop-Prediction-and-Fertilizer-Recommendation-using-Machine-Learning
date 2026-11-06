"""
Database Initialization Module for AGRI-MITRA
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        from models.database_models import User, CropPrediction, FertilizerPrediction
        db.create_all()

        # Seed initial admin account if not already present
        admin_email = app.config.get('ADMIN_EMAIL', 'admin@agrimitra.com')
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                full_name='System Administrator',
                email=admin_email,
                role='admin',
                phone='+91-9876543210',
                location='Central Control Office'
            )
            admin_pwd = app.config.get('ADMIN_PASSWORD', 'ChangeThisAdminPassword!2026')
            admin_user.set_password(admin_pwd)
            db.session.add(admin_user)
            db.session.commit()
