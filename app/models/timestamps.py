from .db import db
from datetime import datetime


class Timestamps:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def get_timestamp_breakdown(self, property_name):
        attribute = getattr(self, property_name, None)
        if attribute and isinstance(attribute, datetime):
            return {
                "year": attribute.year,
                "month": attribute.month,
                "day": attribute.day,
                "hour": attribute.hour,
                "minute": attribute.minute,
            }

    @property
    def created_at_iso(self):
        if isinstance(self.created_at, datetime):
            return self.created_at.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        return None

    @property
    def updated_at_iso(self):
        if isinstance(self.updated_at, datetime):
            return self.updated_at.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        return None
