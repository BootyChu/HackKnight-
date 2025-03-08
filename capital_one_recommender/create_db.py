from app import create_app
from app.utils.models import db

app = create_app()

with app.app_context():
    db.create_all()

print("✅ New database created!")