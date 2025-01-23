from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cleaner(db.Model):
    __tablename__ = 'cleaners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Cleaner {self.name}>"

class ClientRequest(db.Model):
    __tablename__ = 'client_requests'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ClientRequest {self.id}>"






def match_candidates(requirements):
    # Dummy matching logic
    cleaners = [
        {"name": "Alice", "experience": 5, "location": "City A"},
        {"name": "Bob", "experience": 3, "location": "City B"}
    ]
    # Rank cleaners based on requirements
    ranked_cleaners = sorted(
        cleaners, 
        key=lambda c: (c["experience"] >= requirements["experience"],
                       c["location"] == requirements["location"]),
        reverse=True
    )
    return ranked_cleaners
