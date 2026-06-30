from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime


class Task(Document):
    title = StringField(required=True, max_length=200)
    done = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'tasks',
        'ordering': ['-created_at']
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'done': self.done,
            'created_at': self.created_at.isoformat(),
        }
