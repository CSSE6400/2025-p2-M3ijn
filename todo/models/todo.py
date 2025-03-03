import datetime
from . import db

class Todo(db.Model):
    __tablename__ = 'todos'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Title column (mandatory, max 80 characters)
    title = db.Column(db.String(80), nullable=False)
    
    # Description column (optional, max 120 characters)
    description = db.Column(db.String(120), nullable=True)
    
    # Completed status (default: False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Deadline column (optional)
    deadline_at = db.Column(db.DateTime, nullable=True)
    
    # Created timestamp (default: current UTC time)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # Updated timestamp (auto-updates on modification)
    updated_at = db.Column(db.DateTime, nullable=False, 
                           default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    # Convert model instance to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'deadline_at': self.deadline_at.isoformat() if self.deadline_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Todo {self.id} {self.title}>'