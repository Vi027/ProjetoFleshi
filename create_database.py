from appfleshi import app, database
from appfleshi.models import User, Photo, Like

with app.app_context():
    database.create_all()
