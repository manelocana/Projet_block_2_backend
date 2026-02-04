

from app.extensions import db


# model db pour editer la biographie
class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
