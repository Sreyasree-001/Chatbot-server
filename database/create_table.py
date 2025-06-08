from app import app
from database.extension import db

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
#run "$ python -m database.create_table.py" to create tables